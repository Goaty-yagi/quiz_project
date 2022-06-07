<template>
    <div class='shape-wrapper'>
        <div class="shape-container" ref='text1'>
            <div class="parallel-quadrangle" ref='step1'></div>
            <p v-if='$store.state.step==1'> 情報入力</p>
            <p v-if='$store.state.step!=1'>1</p>
        </div>
        <div class="shape-container" id='second' ref='text2'>
            <div class="parallel-quadrangle" ref='step2'></div>
            <p v-if='$store.state.step!=2'>2</p>
            <p class='ips-text' v-if='$store.state.step==2'>パスワード<wbr>入力</p>
        </div>
        <div class="shape-container" id='three' ref='text3'>
            <div class="parallel-quadrangle" ref='step3'></div>
            <p v-if='$store.state.step!=3'> 3</p>
            <p v-if='$store.state.step==3'>メール承認<wbr></p>
        </div>
        <div class="shape-container" ref='text4'>
            <div class="parallel-quadrangle" ref='step4'></div>
            <p v-if='$store.state.step!=4' id='done'>完了</p>
            <p v-if='$store.state.step==4'>登録完了</p>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            step:''
        }
    },
    beforeMount(){
        // this.step = this.$store.state.step
        // this.classAdder()
        // this.classAdder2()
    },
    mounted(){
        this.classAdder2()
        this.classAdder()
        
        
    },
    methods:{
        classAdder(){
            if (this.$store.state.step == 1){
                this.$refs.step1.classList.add('steps')
            }else if (this.$store.state.step == 2){
                this.$refs.step2.classList.add('steps')
            }else if (this.$store.state.step == 3){
                this.$refs.step3.classList.add('steps')
            }else if (this.$store.state.step == 4){
                this.$refs.step4.classList.add('steps')
            }
            console.log('conte',this.step)
            if(this.$store.state.step == 2){
                this.$refs.step1.classList.add('done')
            }else if (this.$store.state.step ==3){
                this.$refs.step2.classList.add('done')
                this.$refs.step1.classList.add('done')
            }else if (this.$store.state.step == 4){
                this.$refs.step3.classList.add('done')
                this.$refs.step2.classList.add('done')
                this.$refs.step1.classList.add('done')
            }
        },
        classAdder2(){
            if (this.$store.state.step == 1){
                this.$refs.text1.classList.add('text')
            }
            else if (this.$store.state.step == 2){
                this.$refs.text2.classList.add('text')
            }
            else if (this.$store.state.step == 3){
                this.$refs.text3.classList.add('text')
            }
            else if (this.$store.state.step == 4){
                this.$refs.text4.classList.add('text')
            }
        },
    }
}
</script>

<style scoped lang='scss'>
@import "style/_variables.scss";
    .shape-wrapper{
        display:flex;
        align-items: flex-start;
        justify-content: center;
        margin-right:2rem;
        // align-content: stretch; 

    }
    .shape-container{
        margin-left: 4%;
        margin-right: 4%;
        position:relative;
        text-align: center;
        overflow: visible;
        white-space:nowrap;
    }
    .shape-container.text#second p{
        // white-space:initial;
        font-size:0.8rem;
        top:55%;
        line-height:1rem
    }
    .shape-container.text#three p{
        // white-space:initial;
        font-size:0.8rem;
        line-height:1rem
    }
    .shape-container p{
        position:absolute;
        color:rgb(56, 55, 55);
        top: 50%;
        left: 60%;
        font-size:1.5rem;
        font-weight: bold;
    }
    #done{
        left: 45%;
        top: 70%;
        font-size:initial;
    }
    .shape-container.text p{
        position:absolute;
        color:white;
        top: 70%;
        left: 35%;
        font-size:initial;
        font-weight: bold;
    }
    .shape-container.text .id-text{
        left:45%;
    }
    
    .parallel-quadrangle {
        width: 3rem;
        height: 2rem;
        left:20%;
        transform: skewX(25deg);
        position: relative;
        border:solid $base-color;
        border-width: 0.2rem 0.2rem 0 0.2rem;
        background: $back-white;
        }.parallel-quadrangle:after{
            content: "";
            position: absolute;
            width: 3rem;
            height: 2rem;
            left: -1.22rem;
            top: 1.75rem;
            transform: skewX(348grad);
            border:solid $base-color;
            border-width: 0 0.2rem 0.2rem 0.2rem;
            background: $back-white;
            }
    .parallel-quadrangle.steps{
        width: 5rem;
        background: $base-color;
    }
    .parallel-quadrangle.steps:after{
        width: 5rem;
        background: $base-color;
    }
    .parallel-quadrangle.done{
        background:rgba(0,0,0,0.5);
    }
    .parallel-quadrangle.done:after{
        background:rgba(0,0,0,0.5);
    }
    .id-text{
        position:absolute;
        font-size:3rem;
        left:3rem;
    }
</style>