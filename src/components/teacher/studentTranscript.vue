<!-- 学生成绩统计 -->
<template>
    <div class="exam">
      <el-table :data="pagination.records" border>
        <el-table-column fixed="left" prop="source" label="考试名称" width="180"></el-table-column>
        <el-table-column prop="examCode" label="考试编号" width="120"></el-table-column>
        <el-table-column prop="description" label="介绍" width="160"></el-table-column>
        <el-table-column prop="institute" label="所属学院" width="120"></el-table-column>
        <el-table-column prop="major" label="所属专业" width="150"></el-table-column>
        <el-table-column prop="grade" label="年级" width="120"></el-table-column>
        <el-table-column prop="examDate" label="考试日期" width="120"></el-table-column>
        <el-table-column prop="totalTime" label="持续时间" width="120"></el-table-column>
        <el-table-column prop="totalScore" label="总分" width="120"></el-table-column>
        <!-- <el-table-column prop="type" label="试卷类型" width="120"></el-table-column> -->
        <!-- <el-table-column prop="tips" label="考生提示" width="400"></el-table-column> -->
        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button @click="toRanking(scope.row.examCode,scope.row.source)" type="primary" size="small">查看成绩数据</el-button>
  
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.current"
        :page-sizes="[4, 8, 10, 20]"
        :page-size="pagination.size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total" class="page">
      </el-pagination>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {}, //保存点击以后当前试卷的信息
        pagination: { //分页后的考试信息
          current: 1, //当前页
          total: null, //记录条数
          size: 4 ,//每页条数
          records:[]
        },
        dialogVisible: false
      }
    },
    created() {
      this.getExamInfo()
    },
    methods: {
      getExamInfo() { //分页查询所有试卷信息
        this.$axios(`/teachers/exams/${this.pagination.current}/${this.pagination.size}`).then(res => {
          console.log("进入")
          // console.log(res.data)
          // console.log(res.data.data)
          this.pagination.records = res.data.data.data
          console.log(this.paginatiores.records)
        }).catch(error => {
        })
      },
      //改变当前记录条数
      handleSizeChange(val) {
        this.pagination.size = val
        this.getExamInfo()
      },
      //改变当前页码，重新发送请求
      handleCurrentChange(val) {
        this.pagination.current = val
        this.getExamInfo()
      },
      toRanking(examCode,source) { //跳转到该试卷的成绩排名页面
        this.$router.push({path: '/studentGradeRanking', query:{examCode: examCode, source: source}})
      }
    },
  };
  </script>
  <style lang="less" scoped>
  .exam {
    padding: 0px 40px;
    .page {
      margin-top: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .edit{
      margin-left: 20px;
    }
  }
  </style>
  