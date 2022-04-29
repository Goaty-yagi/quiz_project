<template>
    <div class='testresult-wrapper'>
        <h1 class='is-size-1 has-text-white'>-結果-</h1>
        <p class='result-text'>あなたのレベルは…</p>
        <div class="diamond-wrapper">
            <div class='dwrapper1'>
                <div class='diamond-outer'/>
            </div>
            <div class='dwrapper2'>
                <div class='diamond'/>
            </div>
            <div class='text-wrapper'>
                <p class='text'>{{ finalResult.grade }}</p>
                <p class='level-text'>Lv,{{ finalResult.level }}</p>
            </div>
        </div>
        <div class='font-wrapper'>
            <i class="fab fa-angellist"></i>
        </div>
        <transition name="notice">
            <Notification
            v-if="showNotification"/>
        </transition>
    </div>
</template>

<script>
import Notification from '@/components/initial/Notification.vue'
export default {
    props:[
        "finalResult"
    ],
     components: {
        Notification,
  },
  data(){
        return{
            showNotification: false,
        }
    },
    mounted(){
        console.log('testresult')
        setTimeout(() =>{
        this.handleShowNotification()
        },3000)
    },
    methods:{
        handleShowNotification(){
        this.showNotification = !this.showNotification
    }
    }
}
</script>

<style scoped lang="scss">
.testresult-wrapper{
        
}
    /* // this is only for i phone5 */
  @media(max-width: 355px){
      
        .result-text{
            font-size:1.5rem;
            color:white;
            }
        .diamond-wrapper{
            position:relative;
            margin-top:-2rem;
            margin-bottom:auto;    
            }
        .diamond-outer{
            border: 7.5rem solid transparent;
            border-bottom: 5.5rem solid orange;
            position: relative;
            top: -5rem;
            width: 0;
            height: 0;
            margin: 0 auto;
        }
        .diamond-outer:after{
            content: '';
            position: absolute;
            left: -7.5rem;
            top: 5.5rem;
            width: 0;
            height: 0;
            border: 7.5rem solid transparent;
            border-top: 5.5rem solid orange;
                }        
        .diamond{
            width: 0;
            height: 0;
            border: 7rem solid transparent;
            border-bottom: 5rem solid white;
            position: relative;
            top: -17rem;
            margin: 0 auto;
                }
        .diamond:after{
            content: '';
            position: absolute;
            left: -7rem;
            top: 5rem;
            width: 0;
            border: 7rem solid transparent;
            border-top: 5rem solid white;
            }
        .text{
            font-size:2rem;
            color:black;
            font-weight: bold;
            }
        .text-wrapper{
            position:absolute;
            left: 0;
            right: 0;
            margin: 0 auto;
            top:6.5rem;
            }
        .font-wrapper{
            font-size:10rem;
            color:orange;
            margin-top:-13rem;
        }
    }
    @media(min-width: 356px){
    .result-text{
            font-size:2rem;
            color:white;
            }
    .diamond-wrapper{
        position:relative;     
        }
    .dwrapper1{
        position:absolute;
        left: 0;
        right: 0;
        margin: 0 auto;
        
    }
    .dwrapper2{
        position:absolute;
        left: 0;
        right: 0;
        margin: 0 auto;
    }
    .diamond-outer {
        width: 0;
        height: 0;
        border: 8.5rem solid transparent;
        border-bottom: 5.5rem solid orange;
        position: relative;
        top: -5rem;
        margin: 0 auto;

    }   
    .diamond-outer:after {
        content: '';
        position: absolute;
        left: -8.5rem; top:5.5rem;
        width: 0;
        height: 0;
        border: 8.5rem solid transparent;
        border-top: 5.5rem solid orange;
    }

    .diamond {
        width: 0;
        height: 0;
        border: 8rem solid transparent;
        border-bottom: 5rem solid white;
        position: relative;
        top: -4rem;
        margin: 0 auto;
    }
    .diamond:after {
        content: '';
        position: absolute;
        left: -8rem; top:5rem;
        width: 0;
        height: 0;
        border: 8rem solid transparent;
        border-top: 5rem solid white;
        
    }
    .text-wrapper{
        position:absolute;
        left: 0;
        right: 0;
        margin: 0 auto;
        top:7.5rem;
    }
    .text{
        font-size:2rem;
        color:black;
        font-weight: bold;
        margin: 0 auto;
    }
    .level-text{
        font-weight: bold;
        font-size: 1.5rem;
    }
    .font-wrapper{
        font-size:10rem;
        color:orange;
        margin-top:15rem;
    }
}

// .testresult-wrapper{
//     .main-wrapper{
//         .content-wrapper{
//             display: flex;
//             flex-direction: column;
//             .text-wrapper{
//                 .result-text{
//                     color: white;
//                     font-size: 2.5rem;
//                     font-weight: bold;
//                 }
//                 .result-level-text{
//                     color: white;
//                     font-size: 1.5rem;
//                     font-weight: bold;
//                 }
//             }
//             .diamond-wrapper{
//                 position:relative;
//                 display: flex;
//                 justify-content: center;
//                 .dwrapper1{
//                     .diamond-outer{
//                     border: 7.5rem solid transparent;
//                     border-bottom: 5.5rem solid orange;
//                     position: relative;
//                     top: -5rem;
//                     width: 0;
//                     height: 0;
//                     margin: 0 auto;
//                     }
//                     .diamond-outer:after{
//                         content: '';
//                         position: absolute;
//                         left: -7.5rem;
//                         top: 5.5rem;
//                         width: 0;
//                         height: 0;
//                         border: 7.5rem solid transparent;
//                         border-top: 5.5rem solid orange;
//                     }        
//                 }
//                 .dwrapper2{
//                     .diamond{
//                         width: 0;
//                         height: 0;
//                         border: 7rem solid transparent;
//                         border-bottom: 5rem solid white;
//                         position: relative;
//                         top: -17rem;
//                         margin: 0 auto;
//                     }
//                     .diamond:after{
//                         content: '';
//                         position: absolute;
//                         left: -7rem;
//                         top: 5rem;
//                         width: 0;
//                         border: 7rem solid transparent;
//                         border-top: 5rem solid white;
//                     }
//                 }
//             }
//         }
//     }
        
// }

</style>