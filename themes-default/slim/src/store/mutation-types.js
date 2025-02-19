const LOGIN_PENDING = '🔒 Logging in';
const LOGIN_SUCCESS = '🔒 ✅ Login Successful';
const LOGIN_FAILED = '🔒 ❌ Login Failed';
const LOGOUT = '🔒 Logout';
const REFRESH_TOKEN = '🔒 Refresh Token';
const REMOVE_AUTH_ERROR = '🔒 Remove Auth Error';
const SOCKET_ONOPEN = '🔗 ✅ WebSocket connected';
const SOCKET_ONCLOSE = '🔗 ❌ WebSocket disconnected';
const SOCKET_ONERROR = '🔗 ❌ WebSocket error';
const SOCKET_ONMESSAGE = '🔗 ✉️ 📥 WebSocket message received';
const SOCKET_RECONNECT = '🔗 🔃 WebSocket reconnecting';
const SOCKET_RECONNECT_ERROR = '🔗 🔃 ❌ WebSocket reconnection attempt failed';
const NOTIFICATIONS_ENABLED = '🔔 Notifications Enabled';
const NOTIFICATIONS_DISABLED = '🔔 Notifications Disabled';
const ADD_CONFIG = '⚙️ Config added to store';
const UPDATE_LAYOUT_LOCAL = '⚙️ Local layout updated in store';
const ADD_REMOTE_BRANCHES = '⚙️ Add git remote branches to store';
const ADD_SHOW = '📺 Show added to store';
const ADD_SHOW_CONFIG = '📺 Show config updated in store';
const ADD_SHOWS = '📺 Multiple Shows added to store in bulk';
const ADD_SHOW_EPISODE = '📺 Shows season with episodes added to store';
const ADD_STATS = 'ℹ️ Statistics added to store';
const SET_STATS = 'SET_STATS';
const SET_MAX_DOWNLOAD_COUNT = 'SET_MAX_DOWNLOAD_COUNT';
const ADD_SHOW_SCENE_EXCEPTION = '📺 Add a scene exception';
const REMOVE_SHOW_SCENE_EXCEPTION = '📺 Remove a scene exception';
const ADD_HISTORY = '📺 History added to store';
const ADD_HISTORY_ROW = '📺 History row added to store';
const ADD_SHOW_HISTORY = '📺 Show specific History added to store';
const ADD_SHOW_EPISODE_HISTORY = "📺 Show's episode specific History added to store";
const ADD_PROVIDER = '⛽ Provider added to store';
const ADD_PROVIDERS = '⛽ Provider list added to store';
const ADD_PROVIDER_CACHE = '⛽ Provider cache results added to store';
const ADD_SEARCH_RESULTS = '⛽ New search results added for provider';
const ADD_QUEUE_ITEM = '🔍 Search queue item updated';
const ADD_SHOW_QUEUE_ITEM = '📺 Show queue item added to store';
const REMOVE_SHOW = '📺 Show removed from store';
const REMOVE_PROVIDER = '⛽ Provider removed';
const UPDATE_SHOWLIST_DEFAULT = '⚙️ Anime config showlist default updated';
const ADD_SCHEDULE = '📅 Schedule information added';

export {
    LOGIN_PENDING,
    LOGIN_SUCCESS,
    LOGIN_FAILED,
    LOGOUT,
    REFRESH_TOKEN,
    REMOVE_AUTH_ERROR,
    SOCKET_ONOPEN,
    SOCKET_ONCLOSE,
    SOCKET_ONERROR,
    SOCKET_ONMESSAGE,
    SOCKET_RECONNECT,
    SOCKET_RECONNECT_ERROR,
    NOTIFICATIONS_ENABLED,
    NOTIFICATIONS_DISABLED,
    ADD_CONFIG,
    UPDATE_LAYOUT_LOCAL,
    ADD_HISTORY,
    ADD_HISTORY_ROW,
    ADD_SHOW,
    ADD_SHOW_CONFIG,
    ADD_SHOWS,
    ADD_SHOW_EPISODE,
    ADD_STATS,
    ADD_REMOTE_BRANCHES,
    SET_STATS,
    SET_MAX_DOWNLOAD_COUNT,
    ADD_SHOW_SCENE_EXCEPTION,
    REMOVE_SHOW_SCENE_EXCEPTION,
    ADD_SHOW_HISTORY,
    ADD_SHOW_EPISODE_HISTORY,
    ADD_PROVIDER,
    ADD_PROVIDERS,
    ADD_PROVIDER_CACHE,
    ADD_SEARCH_RESULTS,
    ADD_QUEUE_ITEM,
    ADD_SHOW_QUEUE_ITEM,
    REMOVE_SHOW,
    REMOVE_PROVIDER,
    UPDATE_SHOWLIST_DEFAULT,
    ADD_SCHEDULE
};
