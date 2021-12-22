import createPersistedState from 'vuex-persistedstate'
import { auth } from '@/firebase/config'
import {
  createUserWithEmailAndPassword,
  fetchSignInMethodsForEmail,
  EmailAuthProvider
} from 'firebase/auth'

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
        password:'',
        user: null,
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
        },
        setUser(state,payload){
            state.user = payload
            console.log('user state changed:',state.user)
        }
    },
    actions:{
        async signup(context, {email,password}){
            console.log('signup in')
            const ref = await createUserWithEmailAndPassword(auth, email, password)
            try{
                console.log('try signup in')
                context.commit('setUser',ref.user)
            }catch{
                console.log('error in sign up')
                throw new Error('could not conmplite signin')
            }
        },
        async checkEmail(context,email){
            const ref = await fetchSignInMethodsForEmail(auth,email);
            if (ref == 'password'){
                console.log('already in use')
            }else{
                console.log('you can use it')
            }
            
                console.log('checkmail',ref ,ref == 'password')
                // console.log('checkmail2','fulfilled' in(await ref),(await ref).includes(['Promise'])  )
                    
        }
    }

}