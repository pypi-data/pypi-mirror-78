import gym
import asyncio
import os
from typing import List, Dict, Tuple
import sys

# This is a copy of the pyppeteer function in pyppeteer/chromium_downloader,
# but since we're trying to update the environment variables which are read in that file
# we can't import it
def pyppeteer_current_platform() -> str:
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    elif (sys.platform.startswith('win') or
          sys.platform.startswith('msys') or
          sys.platform.startswith('cyg')):
        if sys.maxsize > 2 ** 31 - 1:
            return 'win64'
        return 'win32'
    raise OSError('Unsupported platform: ' + sys.platform)

if not ('PYPPETEER_CHROMIUM_REVISION' in os.environ):
  plt = pyppeteer_current_platform()
  if plt == 'win32':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798057'
  elif plt == 'win64':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '803555'
  elif plt == 'linux':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798580'
  elif plt == 'mac':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798027'
if not ('PYPPETEER_DOWNLOAD_HOST' in os.environ):
  os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'http://storage.googleapis.com'
import pyppeteer
import numpy as np
from random import random
import webbrowser
import base64
import logging

logger = logging.getLogger(__name__)

class BattleConnectionError(Exception):
  def __init__(self):
    pass

class DerkEnv(gym.Env):
  """Reinforcement Learning environment for "Dr. Derk's Mutant Battlegrounds"

  The environment can be run in one of two modes: 'train' or 'battle'. In 'train'
  you control both the home and away team. In 'battle' you are matched against
  an opponent on the internet, to see how well your agent performs compared to
  that agent.

  Args:
    mode: Either 'train' or 'battle'. (Environment variable: DERK_MODE)
    host: Configure an alternative game host. (Environment variable: DERK_HOST)
    home_team: Home team creatures
    away_team: Away team creatures
    reward_function: Reward function. See :ref:`reward-function` for available options
    dummy_mode: Don't actually run the game, but just return random outputs
    n_arenas: Number of parallel arenas to run
    substeps: Number of game steps to run for each call to step
    api_key: Api key to use for battling. (Environment variable: DERK_API_KEY)
    turbo_mode: Skip rendering to the screen to run as fast as possible. (Environment variable: DERK_TURBO_MODE)
    interleaved: Run each step in the background, returning the previous steps observations
    opponent_limit: Maximum number of times you will be matched with the same user & agent_version in battle mode
    team_id: Team to use when battling. (Environment variable: DERK_TEAM_ID)
    agent_version: A unique version identifier for the current agent. Used for opponent_limit
    headless: Run in headless mode
    chrome_executable: Path to chrome or chromium. (Environment variable: DERK_CHROME_EXECUTABLE)
    chrome_args: List of command line switches passed to chrome
    browser: A pyppeteer browser instance
    safe_reset: A safer but slower version of reset. Use this if you get CONTEXT_LOST errors. (Environment variable: DERK_SAFE_RESET)
    no_init_browser: You need to run env.async_init_browser() manually to launch the browser if this is set to true

  With the interleaved mode on, there's a delay between observation and action of size substeps.
  E.g. if substeps=8 there's an 8*16ms = 128ms "reaction time" from observation to action. This means
  that the game and the python code can in effect run in parallel. This is always enabled in battles.

  """
  def __init__(self, mode: str=None, host: str=None,
      home_team: List[Dict] = None, away_team: List[Dict] = None, reward_function: Dict=None,
      dummy_mode: bool=False, n_arenas: int=1, substeps: int=8, api_key: str=None, turbo_mode: bool=False,
      interleaved: bool=True, opponent_limit: int=20, team_id: str=None, agent_version: str='',
      headless: bool=False, chrome_executable: str=None, chrome_args: List[str]=[], browser: pyppeteer.browser.Browser=None,
      safe_reset: bool=None, no_init_browser: bool=False):
    self.mode = mode if mode is not None else os.environ.get('DERK_MODE', 'train')
    self.host = host if host is not None else os.environ.get('DERK_HOST', ('file://' + os.path.abspath(__file__ + '/../../app_build/index.html')))
    self.home_team = home_team
    self.away_team = away_team
    self.reward_function = reward_function
    self.dummy_mode = dummy_mode
    self.n_arenas = 1 if self.mode == 'battle' else n_arenas
    self.substeps = substeps
    self.api_key = api_key if api_key is not None else os.environ.get('DERK_API_KEY', '')
    self.turbo_mode = turbo_mode if turbo_mode is not None else (os.environ.get('DERK_TURBO_MODE', 'False').lower() == 'true')
    self.interleaved = interleaved
    self.opponent_limit = opponent_limit
    self.team_id = team_id if team_id is not None else os.environ.get('DERK_TEAM_ID', None)
    self.agent_version = agent_version
    self.headless = headless
    self.chrome_executable = chrome_executable if chrome_executable is not None else os.environ.get('DERK_CHROME_EXECUTABLE', None)
    self.chrome_args = chrome_args
    self.browser = browser
    self.safe_reset = safe_reset if safe_reset is not None else (os.environ.get('DERK_SAFE_RESET', 'False').lower() == 'true')

    self.n_agents_per_arena = (6 if self.mode == 'train' else 3)
    self.n_agents = self.n_agents_per_arena * self.n_arenas

    if self.mode == 'battle' and not self.api_key:
      raise Exception('You need an api key and license to battle. You can find your api key on your profile page on https://gym.derkgame.com')

    self.n_senses = 64

    self.observation_space = gym.spaces.Box(low=-1, high=1, shape=[self.n_senses])
    self.action_space = gym.spaces.Tuple((
      gym.spaces.Box(low=-1, high=1, shape=[]), # MoveX
      gym.spaces.Box(low=-1, high=1, shape=[]), # Rotate
      gym.spaces.Box(low=0, high=1, shape=[]), # ChaseFocus
      gym.spaces.Discrete(4), # CastingSlot
      gym.spaces.Discrete(8), # ChangeFocus
    ))

    if (not self.dummy_mode and not no_init_browser):
      asyncio.get_event_loop().run_until_complete(self.async_init_browser())

  def reset(self) -> np.ndarray:
    """Resets the state of the environment and returns an initial observation.

    Returns:
      The initial observation for each agent, with shape (n_agents, n_senses). See :ref:`senses`

    Raises:
      BattleConnectionError: If there was a connection error in battle mode
    """
    return asyncio.get_event_loop().run_until_complete(self.async_reset())

  def step(self, action_n: List[List[float]]) -> Tuple[np.ndarray, np.ndarray, List[bool], List[Dict]]:
    """Run one timestep.

    Accepts a list of actions, one for each agent, and returns the current state

    Args:
      action_n: A list of actions (one per "creature" agent). See :ref:`actions`

    Returns:
      A tuple of (observation_n, reward_n, done_n, info). See :ref:`senses`.
      observation_n has shape (n_agents, n_senses)

    Raises:
      BattleConnectionError: If there was a connection error in battle mode
    """
    return asyncio.get_event_loop().run_until_complete(self.async_step(action_n))

  def close(self):
    """Shut down environment
    """
    return asyncio.get_event_loop().run_until_complete(self.async_close())

  def get_total_reward(self) -> np.ndarray:
    """Total reward earned throughout the entire session for each agent
    """
    return asyncio.get_event_loop().run_until_complete(self.async_get_total_reward())

  async def async_init_browser(self):
    """Creates a browser instance. This only needs to be invoked if no_init_browser was passed to the constructor"""
    logger.info('[init] Using host: ' + self.host)
    if not self.browser:
      logger.info('[init] Creating browser')
      chromium_args = [
        '--app=' + self.host,
        '--allow-file-access-from-files',
        '--disable-web-security',
        '--no-sandbox',
        '--ignore-gpu-blacklist',
        '--user-data-dir=' + os.environ.get('DERK_CHROMEDATA', './chromedata')
      ] + self.chrome_args
      if (self.headless):
        chromium_args.append('--use-gl=egl')
      self.browser = await pyppeteer.launch(
        ignoreHTTPSErrors=True,
        headless=self.headless,
        executablePath=self.chrome_executable,
        args=chromium_args,
        defaultViewport=None
      )
      logger.info('[init] Creating browser ok')
    logger.info('[init] Getting page')
    self.page = (await self.browser.pages())[0]
    backend = os.environ.get('DERK_BACKEND', None)
    if backend is not None:
      logger.info('[init] Setting backend')
      await self.page.evaluateOnNewDocument('''(backend) => window.localStorage.setItem('backend', backend)''', backend)
    logger.info('[init] Exposing license link function')
    await self.page.exposeFunction('openGymLicenses', lambda: webbrowser.open('https://gym.derkgame.com/licenses'))
    logger.info('[init] Setting up logs')
    self.page.on('console', self._handle_console)
    self.page.on('error', lambda m: logger.error('[error] %s', m))
    self.page.on('pageerror', lambda m: logger.error('[pageerror] %s', m))
    self.page.on('requestfailed', lambda m: logger.error('[requestfailed] %s', m))
    logger.info('[init] Navigating to host')
    await self.page.goto(self.host)
    logger.info('[init] Waiting for GymLoaded')
    await self.page.waitForSelector('.GymLoaded')
    logger.info('[init] Gym loaded ok')
    if self.api_key:
      logger.info('[init] Logging in')
      await self.page.evaluate('''apiKey => window.derk.loginWithApiKey(apiKey)''', self.api_key)
    logger.info('[init] Getting sense count')
    self.n_senses = await self.page.evaluate('''() => window.derk.nSenses''')
    logger.info('[init] Done!')

  def _handle_console(self, m):
    if m.type == 'error':
      logger.error('[console] %s', m.text)
    elif m.type == 'warning':
      logger.warning('[console] %s', m.text)
    else:
      logger.info('[console] %s', m.text)

  async def async_reset(self):
    """Async version of :meth:`reset`"""
    logger.info('[reset] Resetting...')
    if self.dummy_mode:
      return [self.observation_space.sample() for i in range(self.n_agents)]
    if self.safe_reset:
      logger.info('[reset] Running safe reset (reload page)')
      await self.page.reload()
      logger.info('[reset] Waiting for GymLoaded')
      await self.page.waitForSelector('.GymLoaded')
    config = {
      'mode': self.mode,
      'home': self.home_team,
      'away': self.away_team,
      'rewardFunction': self.reward_function,
      'nArenas': self.n_arenas,
      'substeps': self.substeps,
      'turboMode': self.turbo_mode,
      'interleaved': self.interleaved,
      'opponentLimit': self.opponent_limit,
      'teamId': self.team_id,
      'agentVersion': self.agent_version,
    }
    observations = self._unwrap_result(await self.page.evaluate('''(config) => window.derk.reset(config)''', config))
    logger.info('[reset] Reset done, decoding observations and returning')
    return self._decode_observations(observations)

  def _unwrap_result(self, res):
    if res['result'] != 'ok':
      if res['error'] == 'connection-error':
        raise BattleConnectionError()
      else:
        raise Exception(res['error'])
    else:
      return res['value']

  async def async_close(self):
    """Async version of :meth:`close`"""
    if not self.dummy_mode:
      await self.browser.close()

  async def async_step(self, action_n):
    """Async version of :meth:`step`"""
    actions_arr = np.asarray(action_n, dtype='float32')
    actions_arr[:, 3] -= 1 # CastingSlot. -1 means no action, but gym.spaces.Discrete starts at 0
    actions_arr[:, 4] -= 1 # ChangeFocus. Same as above

    # Transpose so we get things layer by layer for WebGL
    actions_arr = actions_arr.transpose().reshape(-1)
    base64_actions = base64.b64encode(actions_arr).decode('utf-8')
    if self.dummy_mode:
      return (
        [self.observation_space.sample() for i in range(self.n_agents)],
        [random() for i in range(self.n_agents)],
        [False for i in range(self.n_agents)],
        [{} for i in range(self.n_agents)],
      )
    res = self._unwrap_result(await self.page.evaluate('''(actions) => window.derk.step(actions)''', base64_actions))
    return self._decode_observations(res['observations']), self._decode_reward(res['reward']), res['done'], res['info']

  async def async_get_total_reward(self):
    """Async version of :meth:`get_total_reward`"""
    reward = await self.page.evaluate('''() => window.derk.getTotalReward()''')
    return self._decode_reward(reward)

  def get_webgl_renderer(self) -> str:
    """Return which webgl renderer is being used by the game"""
    return asyncio.get_event_loop().run_until_complete(self.async_get_webgl_renderer())

  async def async_get_webgl_renderer(self):
    """Async version of :meth:`get_webgl_renderer`"""
    return await self.page.evaluate('''() => window.derk.getWebGLRenderer()''')

  def _decode_observations(self, observations):
    obs = np.frombuffer(base64.b64decode(observations), dtype='float32')
    # Images/textures in WebGL are layed out in layer for z, and 4 components per channel
    return obs.reshape((-1, self.n_agents, 4)).swapaxes(0, 1).reshape((self.n_agents, -1))

  def _decode_reward(self, reward):
    return np.frombuffer(base64.b64decode(reward), dtype='float32')
