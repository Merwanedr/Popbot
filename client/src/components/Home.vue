<template>
  <div>
    <!-- Titles -->
    <div class="animated rubberBand title">
      <div id="popbotTitle">P O P B O T</div>
    </div>
    <div id="description">Let AI transform your images.</div>

    <div class="main">
      <div class="optionButtons">
            <input style="display: none;" type="file" @change="onFileSelected" ref="pictureInput" accept="image/gif, image/jpeg, image/png">
            <button @click="$refs.pictureInput.click()" class="uploadPhoto" id="myPicture">Choose a picture</button>
            <br>
            <br>
            <v-btn @click="onUpload" title="Fire!" fab color="white" depressed small><div style="color: #ec6041;"><v-icon dark>send</v-icon></div></v-btn>
            <br>
            <br>
            <div style="color: white; "><strong>{{ pleaseWait }}</strong></div>
            <div style="color: white; "><strong>{{ status }}</strong></div>
          </div>
    </div>
    <v-footer class="pa-3" fixed color="#ec6041" style="text-align: center;">
      <v-layout row>
        <v-flex xs2></v-flex>
         <v-flex xs8><strong><a href="http://www.github.com/Merwanedr/popbot" target="_blank"><div style="color: white;">&copy; {{ new Date().getFullYear() }} Merwane Draï</div></a></strong></v-flex>
         <!-- Just kidding, no copyrights here -->
         <v-flex xs2></v-flex>
      </v-layout>
  </v-footer>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Home',
  data() {
    return {
      selectedFile: null,
      status: '',
      pleaseWait: ''
    }
  },
  methods: {
    onFileSelected(event){
      this.selectedFile = event.target.files[0]
    },
    onUpload() {
      const fd = new FormData();
      fd.append('file', this.selectedFile, this.selectedFile.name);
      this.pleaseWait = 'Please wait...';
      axios.post('http://127.0.0.1:5000/', fd)
      .then(res => {
        this.pleaseWait = '';
        this.status = 'Your transformed picture has been saved on the uploads directory (server).';
        console.log(res);
        this.selectedFile = null;
      })
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a{
  text-decoration: none;
  color: white;
}
a:visited{
  text-decoration: none;
  color: white;
}
.title{
  text-align: center;
  font-family: 'Ubuntu', sans-serif;
  color: white;
  margin-top: 40px;
  animation-delay: 2s;
  animation-iteration-count: 2;
}
#popbotTitle{
  text-align: center;
  font-family: 'Ubuntu', sans-serif;
  color: white;
  font-size: 30px;
}
#description{
  color: white;
  font-family: 'Ubuntu', sans-serif;
  text-align: center;
  margin-top: 10px;
  font-size: 15px;
}
.main{
  margin-top: 30px;
}
.optionButtons{
  position: fixed;
  text-align: center;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.subjectSelect{
  background-color: white;
  border: none;
  border-radius: 50px;
  margin-top: 15px;
  width: 200px;
  height: 30px;
  padding-left: 50px;
  resize: none;
  padding-top: 1px;
  color: #ec6041;
  text-align: center;
}
.subjectSelect:focus{
  outline: none;
}
.uploadPhoto{
  background-color: white;
  border: none;
  border-radius: 50px;
  margin-top: 15px;
  width: 200px;
  height: 30px;
  padding-left: 5px;
  resize: none;
  padding-top: 1px;
  color: #ec6041;
  text-align: center;
}
.uploadPhoto:focus{
  outline: none;
}
</style>
