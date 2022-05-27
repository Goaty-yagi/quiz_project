import createPersistedState from 'vuex-persistedstate'
import Cookies from 'js-cookie'
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
        registeredUser: false,
        djangoUser: null,
        UID:'',
        fasvoriteQuestion:'',
        emailVerified:null,
        authIsReady:false,
        checkedEmail:null,
        accountURL:'http://localhost:8080/',
        actionCodeSettings:{
            url: null,
            handleCodeInApp: true
        },
        tempUser: {
            test: false,
            statusList:'',
            grade:'',
            level:''
        },
        favoriteQuestion:'',
        logger:{
            actualError:'',
            message:'',
            name:''
        },
        userInfo:'',
        exceptUserInfo:'',
        beingException:false,
        reloadForException: false,
        apiError:{
            // this is for connection Error
            django: false,
            firebase: false,
            ipinfo: false,
            any: false
        },
        onSigningup:false,
        myQuestion:'',
        myQuizInfo:{
            id:'',
            max:'',
        },
        gradeDict:{
            '超初級':0,
            '初級':10,
            '中級':20,
            '上級':30
        }
    },
    getters:{
        getUID(state){
            return state.UID
        },
        getUser(state){
            return state.user
        },
        getDjangouser(state){
            return state.djangoUser
        },
        getEmailVerified(state){
            return state.emailVerified
        },
        getTempUser(state){
            return state.tempUser
        },
        logger(state){
            return state.logger
        },
        onSigningup(state){
            return state.onSigningup
        },
        getMyQuestion(state){
            return state.myQuestion
        },
        getMyQuizInfo(state){
            return state.myQuizInfo
        },
        quizNameIdInSignup(state, getters, rootState){
            return rootState.quiz.quizNameId
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
            if(state.user){
                state.registeredUser = true
                state.UID = state.user.uid
            }
            console.log('user state changed:',state.user)
        },
        setAuthIsReady(state,payload){
            state.authIsReady = payload
            console.log('setauth is changed:',state.user)
        },
        setDjangoUser(state,payload){
            state.djangoUser = payload
            console.log('set Django user',state.djangoUser)
        },
        emailVerifiedHandler(state,payload){
            state.emailVerified = payload
            console.log('emailV chainged',state.emailVerified)
        },
        checkEmailHandler(state,payload){
            state.checkedEmail = payload
        },
        setTempUser(state,payload){
            state.tempUser.test = true
            state.tempUser.statusList = payload.status
            state.tempUser.grade = payload.grade
            state.tempUser.level = payload.level
            console.log('set-temp-user', state.tempUser)
        },
        setTempUserReset(state){
            state.tempUser.test = false
            state.tempUser.statusList = '',
            state.tempUser.grade = '',
            state.tempUser.level = ''
            Cookies.remove('tempKey')
            console.log('reset-TempUser',state.tempUser)
        },
        tempUserTestTrue(state){
            state.tempUser.test = true
        },
        resetQuizKeyStorage(state){
            // this is for log out
            state.UID = null
            state.djangoUser = null
            state.emailVerified = null
            state.beingException = false,
            state.reloadForException = false
            state.apiError.django = false
            state.apiError.firebase = false
            state.apiError.ipinfo = false
            state.apiError.any = false
            state.myQuizInfo.id = ''
            state.myQuizInfo.max = ''
            state.myQuestion = ''
            state.registeredUser = false
            console.log('all-Reset')
        },
        setLogger(state,payload){
            state.logger.actualError = payload.actualError
            state.logger.name = payload.name
            state.logger.message = payload.message
        },
        setUserInfo(state,payload){
            state.userInfo = payload
        },
        checkBeingException(state,payload){
            if(state.user&&!state.djangoUser){
                state.beingException = true
                console.log('set-being-exception',state.beingException)
            }
        },
        reloadForExceptionTrue(state){
            if(state.user&&!state.djangoUser){
                state.reloadForException = true
                console.log('setRUFEtrue')
            }
        },
        reloadForExceptionFalse(state){
            state.reloadForException = false
            console.log('setRUFEfalse')
        },
        handleapiError(state,payload){
            if(payload=='django'){
                state.apiError.django = true
            }
            else if(payload=='firebase'){
                state.apiError.firebase = true
            }
            else if(payload=='ipinfo'){
                state.apiError.ipinfo = true
            }
        },
        checkDjangoError(state,payload){
            console.log('checkDE',payload)
            if(state.apiError.django){
                router.push({ name: 'ConnectionError' })
            }
            else if(payload=="Network Error"){
                state.apiError.django = true
                state.apiError.any = true
            }else{
                router.push({ name: 'NotFound404' })
            }
        },
        resetDjangoError(state){
            state.apiError.django = false
            state.apiError.any = false
        },
        handleOnSigningup(state){
            state.onSigningup = !state.onSigningup
        },
        deleteMyQuestion(state,payload){
            console.log("before",state.myQuestion,payload)
            state.myQuestion = state.myQuestion.filter(item =>{
                console.log('item',item)
                return (item.question.id !=payload)
            })
            console.log("after",state.myQuestion)
        },
        addMyQuestion(state,payload){
            console.log("before",state.myQuestion,payload)
            state.myQuestion.push(payload)
            console.log("after",state.myQuestion)
        },
        updateQuizTaker(state,payload) {
            state.djangoUser.quiz_taker[0].grade = payload.grade
            state.djangoUser.quiz_taker[0].level = payload.level
            console.log('set', state.djangoUser)
        },
        updateQuizTakerMax(state, payload) {
            // this is for session storage only to reduce API hit
            state.djangoUser.quiz_taker[0].max_level = state.djangoUser.quiz_taker[0].level
            state.djangoUser.quiz_taker[0].max_grade = payload
                    
            console.log('set_max', state.djangoUser)
        },
    },
    actions:{
        async signupDjangoUser( {state, commit},payload ){
            console.log("INSDU",payload)
            try{
                // throw new Error('could not sent validation')
                await axios({
                    method: 'post',
                    url: '/api/user/',
                    data: payload
                })
                .then(response => {
                    commit('setDjangoUser',response.data)
                })
                state.beingException = false
                commit("resetDjangoError")
                commit("setTempUserReset")
                state.userInfo = ''
            }
            catch(e){
                state.userInfo = payload
                let logger = {
                    message: "in store/signup.getDjangoUser. couldn't signup django user",
                    name: window.location.pathname,
                    actualError: e
                }
                commit('setLogger',logger)
                commit("checkDjangoError", e.message)
            }
        },
        async signupDjangoUserForException( {state, commit},payload ){
            // this is only for unsub below. dont use other part
            console.log("INSDUFX")
            if(!state.djangoUser&&state.beingException){
                if(state.userInfo){
                    try{
                        // throw new Error('could not sent validation')
                        await axios({
                            method: 'post',
                            url: '/api/user/',
                            data: state.userInfo
                        })
                        .then(response => {
                            commit('setDjangoUser',response.data)
                        })
                        state.beingException = false
                        commit('resetDjangoError')
                        commit("setTempUserReset")
                        state.userInfo = ''
                    }
                    catch(e){
                        console.log('catchdayo',e.message)
                        commit("checkDjangoError", e.message)
                        let logger = {
                            message: "in store/signup.getDjangoUserForException. couldn't signup django user",
                            name: window.location.pathname,
                            actualError: e
                        }
                        commit('setLogger',logger)
                        commit("checkDjangoError", e.message)
                    }
                }
                else{
                    try{
                        console.log('NO TEMP')
                        await axios
                        .get("https://ipinfo.io/json?token=32e16159d962c5")
                        .then(response => {
                            let IP = response.data
                            state.exceptUserInfo = {
                                UID: state.user.uid,
                                name: '名前を変更しよう',
                                email: state.user.email,
                                ip_data: [{
                                    city: IP.city,
                                    ip: IP.ip,
                                    loc: IP.loc,
                                    org: IP.org,
                                    postal: IP.postal,
                                    region: IP.region,
                                    timezone: IP.timezone,
                                    country: IP.country
                                }]
                            } 
                        })
                    }
                    catch(e){
                        commit("checkDjangoError", e.message)
                        let logger = {
                            message: "in store/signup.signup.DjangoUserForException. ipinfo error",
                            name: window.location.pathname,
                            actualError: e
                        }
                        commit('setLogger',logger)
                        router.push({ name: 'NotFound404' })
                    }
                     
                    try{
                        console.log('try non_userINFO',state.exceptUserInfo)
                        // throw new Error('could not sent validation')
                        await axios({
                            method: 'post',
                            url: '/api/user/',
                            data: state.exceptUserInfo
                        })
                        state.beingException = false
                        commit("resetDjangoError")
                    }
                    catch(e){
                        commit("checkDjangoError", e.message)
                        let logger = {
                            message: "in store/signup.getDjangoUserForException. couldn't signup django user",
                            name: window.location.pathname,
                            actualError: e
                        }
                        commit('setLogger',logger)
                        router.push({ name: 'NotFound404' })
                    }
                }   
            }
        },
        async getDjangoUser({ state, commit,dispatch }){
            if(state.user&&!state.beingException){
                console.log('GDU_pass',state.beingException)
                try{
                    await axios
                    .get(`/api/user/${state.user.uid}`)
                    .then(response => {
                        commit('setDjangoUser',response.data)
                        state.myQuestion = response.data.my_quiz[0].my_question
                        state.myQuizInfo.id = response.data.my_quiz[0].id
                        state.myQuizInfo.max = response.data.my_quiz[0].max_num
                        console.log("MQ",state.myQuestion)
                    })
                    commit("resetDjangoError")
                }
                catch(e){
                    console.log('catch')
                    let logger = {
                        message: "in store/signup.getDjangoUser. couldn't get django user",
                        name: window.location.pathname,
                        actualError: e
                    }
                    commit('setLogger',logger)
                    commit("checkDjangoError", e.message)
                }
            }
        },
        async getFavoriteQuestion({ state, commit }){
            state.favoriteQuestion = null
            if(state.djangoUser){
                try{
                    const questionId = []
                    for(let i of state.djangoUser.favorite_question[0].question){
                        questionId.push(i)
                    }
                    if(questionId[0]){
                        await axios
                        .get(`/api/board/question-favorite?question_id=${questionId}`)
                        .then(response => {
                            state.favoriteQuestion = response.data
                            })
                        .catch(error => {
                            console.log(error)
                        })
                    }
                }catch{
                    
                }
            }
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
            }catch(e){
                let logger = {
                    message: "in store/signup.signup. couldn't signup firebase user",
                    name: window.location.pathname,
                    actualError: e
                }
                context.commit('setLogger',logger)
                router.push({ name: 'NotFound404' })
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
            // context.commit('setIsLoading', true, {root:true})
            console.log('in_login')
            try{
                var ref = await signInWithEmailAndPassword(auth, email, password)
            }catch{
                console.log('error')
                throw new Error('could not complite signin')
            }
            if(ref){
                console.log("IF YES")
                context.commit('setUser',ref.user)
                context.dispatch('getDjangoUser')
                context.commit("setTempUserReset")
                context.commit('emailVerifiedHandler',ref.user.emailVerified)
                console.log(context.state.user,context.state.emailVerified)
            }else{
                console.log('error in sign in')
                throw new Error('could not complite signin')
            }
            // context.commit('setIsLoading', false, {root:true})                
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
            context.commit('resetQuizKeyStorage')
            router.push({ name: 'Home' })
        },
        updateQuizTakerAction({state, commit, getters},payload){
            console.log('inUQTA',getters)
            commit('updateQuizTaker',payload);
            console.log('UPaction',getters.quizNameIdInSignup)
            for(let i of getters.quizNameIdInSignup){
                if(i.id == payload.grade){
                    if(state.gradeDict[state.djangoUser.quiz_taker[0].max_grade] < state.gradeDict[i.name]){
                        commit('updateQuizTakerMax',i.name);
                        break
                    }
                    else if(state.gradeDict[state.djangoUser.quiz_taker[0].max_grade] == state.gradeDict[i.name]){
                        if(state.djangoUser.quiz_taker[0].max_level < payload.level){
                            commit('updateQuizTakerMax',i.name);
                            break
                        }
                    }
                }
            }
        },
        
    }

}
const unsub = onAuthStateChanged(auth,(user) =>{
    store.commit('setAuthIsReady',true)
    store.commit('setUser',user)
    console.log('unsub')
    if(user){
        store.dispatch('getDjangoUser')
        store.commit('emailVerifiedHandler',user.emailVerified)
        store.dispatch('signupDjangoUserForException')
    }else{
        store.commit('resetQuizKeyStorage')
    }
    unsub()
})