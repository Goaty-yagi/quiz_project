<template>
  <div class="id-wrapper">
      <div class='id-container'>
        <p class='id-text'>送られた６桁のIDを入力してください。</p>
        <p>※半角数字で入力してください。</p>
        <form class="id-form" @submit.prevent='submitForm'>
            <input class='digit' type="text" ref='digit1' maxlength="1" onfocus="this.select();" oninput="this.value=this.value.replace(/[^0-9]/g,'');" v-model='digit1'/>
            <input class='digit' type="text" ref='digit2' maxlength="1" onfocus="this.select();" oninput="this.value=this.value.replace(/[^0-9]/g,'');" v-model='digit2'/>
            <input class='digit' type="text" ref='digit3' maxlength="1" onfocus="this.select();" oninput="this.value=this.value.replace(/[^0-9]/g,'');" v-model='digit3'/>
            <input class='digit' type="text" ref='digit4' maxlength="1" onfocus="this.select();" oninput="this.value=this.value.replace(/[^0-9]/g,'');" v-model='digit4'/>
            <input class='digit' type="text" ref='digit5' maxlength="1" onfocus="this.select();" oninput="this.value=this.value.replace(/[^0-9]/g,'');" v-model='digit5'/>
            <input class='digit' type="text" ref='digit6' maxlength="1" onfocus="this.select();" oninput="this.value=this.value.replace(/[^0-9]/g,'');" v-model='digit6'/>
            <div v-if='idError' class='error'>{{ idError }}</div>
            <div>
                <button class='fbottun' ref='bform'><p>次へ</p></button>
            </div>
        </form>
      </div>
  </div>
</template>

<script>
export default {
    data(){
        return{
            sixDigit:{
                '1':'',
                '2':'',
                '3':'',
                '4':'',
                '5':'',
                '6':'',
            },
            sixDigitList:[],
            digit1:'',
            digit2:'',
            digit3:'',
            digit4:'',
            digit5:'',
            digit6:'',
            fullLength: true,
            idError:'',
            correctID:[1,2,3,4,5,6]
        }
    },
    mounted(){
        // console.log('mounted',this.$refs.digit1.value)
        this.$refs.digit1.focus()
    },
    updated(){
        this.checkSixDigit()
        this.makeSixDigit()
        console.log(this.sixDigit)
    },
    watch:{
        digit1:function(v) { if (v.length == 1) { this.$refs.digit2.focus() } },
        digit2:function(v) { if (v.length <= 1) { this.$refs.digit3.focus() } },
        digit3:function(v) { if (v.length <= 1) { this.$refs.digit4.focus() } },
        digit4:function(v) { if (v.length <= 1) { this.$refs.digit5.focus() } },
        digit5:function(v) { if (v.length <= 1) { this.$refs.digit6.focus() } },
        digit6:function(v) { if (v.length <= 1) { this.$refs.bform.focus() } },
        fullLength:function(v) {if (v == false) { this.$refs.bform.classList.add('button-hover')}
        else{this.$refs.bform.classList.remove('button-hover')}},
    },
    methods:{
        checkSixDigit(){
            console.log('digimetho')
            if (!isNaN(this.digit1)&&this.digit1!=''&&
                !isNaN(this.digit2)&&this.digit2!=''&&
                !isNaN(this.digit3)&&this.digit3!=''&&
                !isNaN(this.digit4)&&this.digit4!=''&&
                !isNaN(this.digit5)&&this.digit5!=''&&
                !isNaN(this.digit6)&&this.digit6!=''){
                    this.fullLength = false
                }
            else{this.fullLength = true}
        },
        makeSixDigit(){
            this.sixDigit[1] = this.digit1
            this.sixDigit[2] = this.digit2
            this.sixDigit[3] = this.digit3
            this.sixDigit[4] = this.digit4
            this.sixDigit[5] = this.digit5
            this.sixDigit[6] = this.digit6
        },
        makeSixDigitList(){
            for (let i in this.sixDigit){
                this.sixDigitList.push(Number(this.sixDigit[i]))
            }
        },
        allclear(){
            this.digit1 =''
            this.digit2 =''
            this.digit3 =''
            this.digit4 =''
            this.digit5 =''
            this.digit6 =''

        },
        submitForm(){
            // validate email
            this.makeSixDigitList()
            this.idError = this.arrayEqual(this.sixDigitList,this.correctID)?
            '' : 'ID is not correct'
            if (this.idError == ''){
                this.$emit('handle')
                this.$store.commit('addStep')
            }else{
                this.sixDigitList=[]
                this.allclear()
            }
        },
        arrayEqual(array1,array2){
            if (!Array.isArray(array1))    return false;
            if (!Array.isArray(array2))    return false;
            if (array1.length != array2.length) return false;
            for (var i = 0, n = array1.length; i < n; ++i) {
                if (array1[i] !== array2[i]) return false;
            }
            return true;
        },
        // getClass(){
        //     if (this.fullLength == false){
        //         this.$refs.buttonHover.classList.add('button-hover')
        //     }else{
        //         this.$refs.buttonHover.classList.remove('button-hover')
        //     }   
        // },
        // nextfocus(){
        //     if (this.$refs.digit1.value!='' && this.sixDigit['1']==''){
        //         this.$refs.digit1.blur()
        //         this.$refs.digit2.focus()
        //     }
        //     else if(this.$refs.digit2.value!=''&& this.sixDigit['2']==''){
        //             this.$refs.digit2.blur()
        //             this.$refs.digit3.focus()
        //     }
        //     else if(this.$refs.digit3.value!=''){
        //             this.$refs.digit3.blur()
        //             this.$refs.digit4.focus()
        //     }
        //     else if(this.$refs.digit4.value!=''){
        //             this.$refs.digit4.blur()
        //             this.$refs.digit5.focus()
        //     }
        //     else if(this.$refs.digit5.value!=''){
        //             this.$refs.digit5.blur()
        //             this.$refs.digit6.focus()
        //     }
        //     else if(this.$refs.digit6.value!=''){
        //             this.$refs.digit6.blur()
        //             this.$refs.button-hover.focus()
        //     }
        // },
        
        // makeSixDigit(){
        //     if(event.target.value != ''&& this.sixDigit.length < 6){
        //         this.sixDigit.push(event.target.value)
        //     }
        // }
    }
}
</script>

<style lang='scss' scoped>
    .id-wrapper{
        width:100vw;
        height:100vh;
    }
    .id-container{
        display:flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width:100%;
        height:25rem;
    }
    .id-text{
        color:white;    
        margin-bottom:1rem;    
    }
    .id-form{
        height: 15%;
        margin-bottom:2rem; 
        
    }
    .digit{
        width: 3rem; 
        height: 4rem;
        border-radius: 0.8rem;
        font-size:2.5rem;
        text-align: center;
    }
    .error{
        color:red;
        text-align: center;
        font-weight: bold;
        margin-bottom:0.2rem;
        border: 0.1rem solid red;
        background:rgb(243, 214, 214);
        width: 90%;
        margin-left: auto;
        margin-right: auto;
        margin-top:1rem;
        }
    p {
        color:white;
    }
</style>