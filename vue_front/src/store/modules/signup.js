import createPersistedState from 'vuex-persistedstate'

export default {
    namespace: true,
    plugins: [
        createPersistedState({
          key: 'signupKey',  // 設定しなければ'vuex'
          paths: ['username','email','email2','country'],  // 保存するモジュール：設定しなければ全部。
          storage: window.sessionStorage,  // 設定しなければlocalStorage
        })],
    state: {
        username: '',
        email:'',
        email2:'',
        country:'',
        password:''
    },
    mutations:{
        getUsername(state,item){
            state.username = item
        },
        getEmail(state,item){
            state.email = item
        },
        getEmail2(state,item){
            state.email2 = item
        },
        getCountry(state,item){
            state.country = item
        },
        getPassword(state,item){
            state.password = item
        }
    }

}