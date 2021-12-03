import { createStore } from 'vuex'

export default createStore({
    
  state: {
    isLoading: false,
    unko: ['unko']
  },
  mutations: {
    setIsLoading(state, status) {
      state.isLoading = status
    }
  },
  actions: {
  },
  modules: {
  }
})
