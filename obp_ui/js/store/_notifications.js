/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import uuid from 'uuid/v4';

const state = {
  notifications: [],
};

const getters = {
  notifications: (state) => state.notifications,
};

const mutations = {
  addNotification: (state, { payload }) => {
    state.notifications.push(payload);
  },
  // eslint-disable-next-line no-shadow
  removeNotification: (state, { uuid }) => {
    const index = state.notifications.findIndex((n) => n.uuid === uuid);
    if (index > -1) {
      state.notifications.splice(index, 1);
    }
  },
};

const actions = {
  addNotification: async (context, { payload }) => {
    payload.uuid = payload.uuid || uuid();
    context.commit('addNotification', { payload });
    if (payload.lifetime) {
      setTimeout(() => {
        context.commit('removeNotification', { uuid: payload.uuid });
      }, payload.lifetime);
    }
  },
  // eslint-disable-next-line no-shadow
  removeNotification: async (context, { uuid }) => {
    context.commit('removeNotification', { uuid });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
