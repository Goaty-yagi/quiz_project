import createPersistedState from 'vuex-persistedstate'
import { auth } from '@/firebase/config'
import {router} from "@/main.js"
import axios from 'axios'
import {
  createUserWithEmailAndPassword,
  fetchSignInMethodsForEmail,
  sendEmailVerification,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  sendPasswordResetEmail
} from 'firebase/auth'
import store from '..'

export default {
    namespace: true,
    // plugins: [
    //     createPersistedState({
    //       key: 'signupKey',  // 設定しなければ'vuex'
    //       paths: ['username','email','email2','country',"UID"],  // 保存するモジュール：設定しなければ全部。
    //       storage: window.sessionStorage,  // 設定しなければlocalStorage
    //     })],
    state: {
        username: '',
        email:'',
        email2:'',
        country:'',
        password:'',
        user: null,
        djangoUser: null,
        UID:'',
        fasvoriteQuestion:'',
        emailVerified:null,
        authIsReady:false,
        checkedEmail:null,
        accountURL:'http://localhost:8080/login/',
        actionCodeSettings:{
            url: null,
            handleCodeInApp: true
                }
    },
    getters:{
        getUID(state){
            return state.UID
        },
        getDjangouser(state){
            return state.djangoUser
        }
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
            state.UID = state.user.uid
            console.log('user state changed:',state.user)
        },
        setAuthIsReady(state,payload){
            state.authIsReady = payload
            console.log('setauth is changed:',state.user)
        },
        emailVerifiedHandler(state,payload){
            state.emailVerified = payload
            console.log('emailV chainged',state.emailVerified)
        },
        checkEmailHandler(state,payload){
            state.checkedEmail = payload
        }
    },
    actions:{
        async getDjangoUser({ state, getters,commit }){
            console.log(getters.getUID)
            await axios
            .get(`/api/user/${getters.getUID}`)
            .then(response => {
                state.djangoUser = response.data
                console.log('inDUGet', state.djangoUser)
                store.dispatch('getFavoriteQuestion')
                })
            .catch(error => {
                console.log(error)
            })
        },
        async getFavoriteQuestion({ state, commit }){
            const questionId = []
            for(let i of state.djangoUser.favorite_question[0].question){
                questionId.push(i.id)
            }
            await axios
            .get(`/api/board/question-favorite?question_id=${questionId}`)
            .then(response => {
                state.favoriteQuestion = response.data
                console.log('inDUGet', state.favoriteQuestion)
                })
            .catch(error => {
                console.log(error)
            })
        },
        async signup(context, {email,password}){
            console.log('signup in')
            try {
                const ref = await createUserWithEmailAndPassword(auth, email, password)
                context.state.actionCodeSettings['url'] = context.state.accountURL
                sendEmailVerification(ref.user,context.state.actionCodeSettings)
                context.commit('setUser',ref.user)
                context.commit('emailVerifiedHandler',ref.user.emailVerified)
                console.log('signup is done',auth.currentUser)
            }catch{
                console.log('error in sign up')
                throw new Error('could not conmplite signup')
            }
        },
        async sendEmailVerify(context){
            context.state.actionCodeSettings['url'] = context.state.accountURL
            console.log('sendEmail',context.state.user,context.state.actionCodeSettings)
            await sendEmailVerification(context.state.user,context.state.actionCodeSettings)
        },
        async sentValidation(context){
            console.log('insentV')
            try{
                await context.state.user.sendEmailVerification()
            }catch{
                console.log('error in sent')
                throw new Error('could not sent validation')
            }
        },
        async login(context, {email,password}){
            const ref = await signInWithEmailAndPassword(auth, email, password)
            context.commit('setUser',ref.user)
            context.commit('emailVerifiedHandler',ref.user.emailVerified)
            console.log(context.state.user,context.state.emailVerified)
                // try{
                //     const ref = await signInWithEmailAndPassword(auth, email, password)
                //     console.log('signin',ref)
                //     
                //     console.log('signin is done',auth.currentUser)
                // }catch{
                //     console.log('catch in store',error.code)
                //     throw new Error('could not complite signin')
                    
                // }
                // if(res){
                //     console.log('signin',ref)
                //     context.commit('setUser',ref.user)
                //     context.commit('emailVerifiedHandler',ref.user.emailVerified)
                //     console.log('signin is done',auth.currentUser)
                // }else{
                //     console.log('error in sign in')
                //     throw new Error('could not complite signin')
                // }
        },
        async checkEmail(context,email){
            try {
                const ref = await fetchSignInMethodsForEmail(auth,email);
                if (ref == 'password'){
                    context.commit('checkEmailHandler',false)
                    console.log('already in use')
                }else{
                    context.commit('checkEmailHandler',true)
                    console.log('you can use it')
                }
            }catch{
                console.log('error in sign up')
                throw new Error('could not check email')
            }
        },
        async passwordReset(context,email){
            console.log('passreset action',email)
            try{
                context.state.actionCodeSettings['url'] = context.state.accountURL
                await sendPasswordResetEmail(auth,email,context.state.actionCodeSettings)
            console.log('password reset sent')
            }catch{
                console.log('error in pass reset')
                throw new Error('could not sent pass reset')
            }
        },
        async logout(context){
            await signOut(auth)
            context.commit('setUser',null)
            router.push({ name: 'Home' })
        }
    }

}
const unsub = onAuthStateChanged(auth,(user) =>{
    store.commit('setAuthIsReady',true)
    store.commit('setUser',user)
    if(user){
        store.dispatch('getDjangoUser')
        store.commit('emailVerifiedHandler',user.emailVerified)
    }
    unsub()
})