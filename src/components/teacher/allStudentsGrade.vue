<!-- 学生成绩查询 -->
<template>
  <div class="all">
    <el-button @click="PageInit()" type="primary" style="float: right; ">查询</el-button>
    <el-input id="inp" v-model="inputCondition" class="w-50 m-2" placeholder="请输入查询学号或名字" :prefix-icon="Search"
      style="float: right;width:200px;" />
    <el-select v-model="clazz" placeholder="请选择班级" style="float: right;width:200px;margin-right: 20px;">
      <el-option value="无"></el-option>
      <el-option v-for="option in clazzOptions" :value="option.clazz" key="clazz" />
    </el-select>
    <label style="float: right;width:50px;font-family: simsun, 宋体, sans-serif;margin-top:11px;">班级:</label>
    <el-select v-model="grade" placeholder="请选择年级" style="float: right;width:200px;margin-right: 20px;">
      <el-option value="无"></el-option>
      <el-option v-for="option in gradeOptions" :value="option.grade" key="grade" />
    </el-select>
    <label style="float: right;width:50px;font-family: simsun, 宋体, sans-serif;margin-top:11px;">年级:</label>
    <el-select v-model="major" placeholder="请选择专业" style="float: right;width:200px;margin-right: 20px;">
      <el-option value="无"></el-option>
      <el-option v-for="option in majorOptions" :value="option.major" key="major" />
    </el-select>
    <label style="float: right;width:50px;font-family: simsun, 宋体, sans-serif;margin-top:11px;">专业:</label>
    <br><br><br>
    <el-table :data="pagination.records" border>
      <el-table-column fixed="left" prop="studentId" label="学号" width="180"></el-table-column>
      <el-table-column prop="studentName" label="姓名" width="200"></el-table-column>
      <el-table-column prop="institute" label="学院" width="200"></el-table-column>
      <el-table-column prop="major" label="专业" width="200"></el-table-column>
      <el-table-column prop="grade" label="年级" width="200"></el-table-column>
      <el-table-column prop="clazz" label="班级" width="100"></el-table-column>
      <el-table-column prop="sex" label="性别" width="120"></el-table-column>
      <el-table-column prop="tel" label="联系方式" width="120"></el-table-column>
      <el-table-column fixed="right" label="查看成绩" width="150">
        <template slot-scope="scope">
          <el-button @click="checkGrade(scope.row.studentId)" type="primary" size="small">查看成绩</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="pagination.current"
      :page-sizes="[6, 10]"
      :page-size="pagination.size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="pagination.total"
      class="page"
    ></el-pagination>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pagination: {
        //分页后的考生信息
        current: 1, //当前页
        total: null, //记录条数
        size: 6,//每页条数
        records:[]
      },
      inputCondition: '',//绑定V-model输入框
      majorOptions: [],
      major: '',
      gradeOptions: [],
      grade: '',
      clazzOptions: [],
      clazz: ''
    };
  },
  created() {
    this.getSpecificStudentInfo();
    // this.getAnswerInfo();
    this.getMajorInfo();
    this.getGradeInfo();
    this.getClazzInfo();
  },
  methods: {
    getClazzInfo() {//班级下拉框
      this.$axios(`/clazz`).then(res => {
        if (res.data.code == '400') {
          console.log("获取信息失败")
        }
        this.clazzOptions = res.data.data;
        console.log(this.clazzOptions)
      }).catch(error => {
        console.log("专业信息请求失败")
      });
    },
    getMajorInfo() {//专业下拉框
      this.$axios(`/major`).then(res => {
        if (res.data.code == '400') {
          console.log("获取信息失败")
        }
        this.majorOptions = res.data.data;
        console.log(this.majorOptions)
      }).catch(error => {
        console.log("专业信息请求失败")
      });
    },
    getGradeInfo() {//年级下拉框
      this.$axios(`/grade`).then(res => {
        if (res.data.code == '400') {
          console.log("获取信息失败")
        }
        this.gradeOptions = res.data.data;
        console.log(this.gradeOptions)
      }).catch(error => {
        console.log("年级信息请求失败")
      });
    },
    // getAnswerInfo() {
    //   //分页查询所有考生信息
    //   this.$axios(`/students/${this.pagination.current}/${this.pagination.size}`).then(res => {
    //     this.pagination.records = res.data.data.data;
    //     console.log(this.pagination);
    //   }).catch(error => {});
    // },
    getSpecificStudentInfo() {//升级版，绑定辅助查询条件
      this.$axios({
        url: '/condition',
        method: 'post',
        data: {
          current: this.pagination.current,
          size: this.pagination.size,
          inputCondition: this.inputCondition,
          major: this.major,
          grade: this.grade,
          clazz: this.clazz,
        }
      }).then(res => {
        if (res.data.code == '400') {
          this.$message({
            type: 'error',
            message: '查询失败！'
          })
        } else {
          this.pagination.records = res.data.data;
          console.log(this.pagination.records)
          this.CurrentSituation = 'specific'
        }
      }).catch(error => {
        console.log("学生信息请求失败")
      });
    },
    //改变当前记录条数
    handleSizeChange(val) {
      this.pagination.size = val;
      this.getSpecificStudentInfo();
    },
    //改变当前页码，重新发送请求
    handleCurrentChange(val) {
      this.pagination.current = val;
      this.getSpecificStudentInfo();
    },
    checkGrade(studentId) {//跳转到成绩折线chart页面
      this.$router.push({ path: "/grade", query: { studentId: studentId } });
      console.log(studentId)
    },
    PageInit() {
      this.pagination.current = 1//将页数跳回至1页
      this.getSpecificStudentInfo();
    },
  }
};
</script>
<style lang="less" scoped>
.all {
  padding: 0px 40px;
  .page {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .edit {
    margin-left: 20px;
  }
  .el-table tr {
    background-color: #dd5862 !important;
  }
}
.el-table .warning-row {
  background: #000 !important;
}

.el-table .success-row {
  background: #dd5862;
}
</style>
