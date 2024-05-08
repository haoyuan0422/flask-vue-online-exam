<!-- 添加考试 -->
<template>
  <section class="add">
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="试卷名称">
        <el-input v-model="form.source" aria-required="true"></el-input>
      </el-form-item>
      <!-- <el-form-item label="介绍">
        <el-input v-model="form.description"></el-input>
      </el-form-item> -->
      <!-- <el-form-item label="所属学院">
        <el-input v-model="form.institute"></el-input>
      </el-form-item> -->
      <el-form-item label="所属专业">
        <el-input v-model="form.major" aria-required="true"></el-input>
      </el-form-item>
      <el-form-item label="年级">
        <el-input v-model="form.grade"></el-input>
      </el-form-item>
      <el-form-item label="考试日期">
        <el-col :span="11">
          <el-date-picker placeholder="选择日期" v-model="form.examDate" style="width: 100%;"></el-date-picker>
        </el-col>
      </el-form-item>
      <el-form-item label="持续时间">
        <el-input v-model="form.totalTime"></el-input>
      </el-form-item>
      <el-form-item label="总分">
        <el-input v-model="form.totalScore"></el-input>
      </el-form-item>
      <el-form-item label="考试类型">
        <el-input v-model="form.type"></el-input>
      </el-form-item>
      <!-- <el-form-item label="考生提示">
        <el-input type="textarea" v-model="form.tips"></el-input>
      </el-form-item> -->
      <el-form-item label="上传试卷">
        <el-input v-model="form.file" type="file" name="file" id="fileInput"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit()">立即创建</el-button>
        <el-button type="text" @click="cancel()">取消</el-button>
      </el-form-item>
    </el-form>
  </section>
</template>

<script>
export default {
  data() {
    return {
      form: { //表单数据初始化
        source: null,
        // description: null,
        // institute: null,
        major: null,
        grade: null,
        examDate: null,
        totalTime: null,
        totalScore: null,
        type: null,
        // tips: null,
        examCode: null,
      }
    };
  },
  methods: {
    formatTime(date) { //日期格式化
      let year = date.getFullYear();
      let month = date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1;
      let day = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
      let hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
      let minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
      let seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
      // 拼接
      return year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
    },
    onSubmit() {
      let examDate = this.formatTime(this.form.examDate)
      this.form.examDate = examDate.substr(0, 10)
      this.$axios(`/GetExamCode`).then(res => {
        this.form.examCode = parseInt(res.data['MAX(examCode)']) + 1 //实现examCode自增1
        this.$axios({
          url: `/exam`,
          method: 'post',
          data: {
            ...this.form
          }
        }).then(res => {
          console.log("addExamInfo=" + res.data)
          if (res.data == '200') {//添加考试信息成功进入下一步
            const axios = require('axios');
            const fileInput = document.querySelector('#fileInput');
            const file = fileInput.files[0];

            const formData = new FormData();
            formData.append('file', file);
            formData.append('source', this.form.source)
            formData.append('examCode', this.form.examCode)
            axios.post('/upload', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }).then(response => {
              console.log("uploadFile=" + response.data)
              if (response.data == 'ok') {
                this.$message({
                  type: 'success',
                  message: '操作成功！'
                })
                this.$router.push({ path: '/selectExam' })
              }
              if (response.data == 'error') {
                this.$message({
                  type: 'error',
                  message: '操作失败！'
                })
              }
            }).catch(error => {
              console.log("uploadFile=未能请求到服务器")
            });
          }
          if (res.data == '400') {
            this.$message({
              type: 'error',
              message: '操作失败！'
            })
          }
        }).catch(error => {
          console.log("addExamInfo=未能请求到服务器")
        })
      })
    },
    cancel() { //取消按钮
      this.form = {}
    },

  }
};
</script>
<style lang="less" scoped>
.add {
  padding: 0px 40px;
  width: 400px;
}
</style>

