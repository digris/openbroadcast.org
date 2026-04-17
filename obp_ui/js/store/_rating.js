/* eslint no-shadow: ["error", { "allow": ["state"] }] */
/* eslint no-param-reassign: ["error", { "ignorePropertyModificationsFor": ["state"] }] */
import Vue from 'vue';
import APIClient from '../api/caseTranslatingClient';


const RATING_ENDPOINT = '/api/v2/rating/rating/';

const parseResponse = (response) => {
  // TODO: update data structure on API (needs update on OBR site as well)
  const { upvotes, downvotes, userVote } = response.data;
  const votes = {
    up: upvotes,
    down: downvotes,
    user: userVote,
  };
  return votes;
};

const state = {
  ratings: [],
};

const getters = {
  ratings: (state) => state.ratings,
  ratingForKey: (state) => (key) => state.ratings.find((r) => r.key === key),
};

const mutations = {
  SET_RATING: (state, { key, votes }) => {
    const index = state.ratings.findIndex((r) => r.key === key);
    if (index > -1) {
      Vue.set(state.ratings, index, { key, votes });
    } else {
      state.ratings.push({ key, votes });
    }
  },
  SET_USER_VOTE: (state, { key, value }) => {
    const index = state.ratings.findIndex((r) => r.key === key);
    if (index > -1) {
      const { votes } = state.ratings[index];
      votes.user = value;
      Vue.set(state.ratings, index, { key, votes });
    } else {
      const votes = {
        user: value,
      };
      state.ratings.push({ key, votes });
    }
  },
};

const actions = {
  loadRating: (context, { key }) => {
    const url = `${RATING_ENDPOINT}${key}/`;
    APIClient.get(url).then((response) => {
      const votes = parseResponse(response);
      context.commit('SET_RATING', { key, votes });
    });
  },
  updateVote: (context, { key, value }) => {
    // immediately set user vote for UI / feedback
    context.commit('SET_USER_VOTE', { key, value });
    const url = `${RATING_ENDPOINT}${key}/`;
    APIClient.put(url, { vote: value }).then((response) => {
      const votes = parseResponse(response);
      context.commit('SET_RATING', { key, votes });
    });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
