// 学生管理页面
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
      <el-table-column fix="left" prop="studentId" label="学号" width="180"></el-table-column>
      <el-table-column prop="studentName" label="姓名" width="180"></el-table-column>
      <el-table-column prop="institute" label="学院" width="200"></el-table-column>
      <el-table-column prop="major" label="专业" width="200"></el-table-column>
      <el-table-column prop="grade" label="年级" width="200"></el-table-column>
      <el-table-column prop="clazz" label="班级" width="100"></el-table-column>
      <el-table-column prop="sex" label="性别" width="120"></el-table-column>
      <el-table-column prop="tel" label="联系方式" width="120"></el-table-column>
      <el-table-column fixed="right" label="操作" width="150">
        <template slot-scope="scope">
          <el-button @click="checkGrade(scope.row.studentId)" type="primary" size="small">编辑</el-button>
          <el-button @click="deleteById(scope.row.studentId)" type="danger" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
      :current-page="pagination.current" :page-sizes="[6, 10]" :page-size="pagination.size"
      layout="total, sizes, prev, pager, next, jumper" :total="pagination.total" class="page">
    </el-pagination>
    <!-- 编辑对话框-->
    <el-dialog title="编辑试卷信息" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
      <section class="update">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="姓名">
            <el-input v-model="form.studentName"></el-input>
          </el-form-item>
          <el-form-item label="学院">
            <el-input v-model="form.institute"></el-input>
          </el-form-item>
          <el-form-item label="专业">
            <el-input v-model="form.major"></el-input>
          </el-form-item>
          <el-form-item label="年级">
            <el-input v-model="form.grade"></el-input>
          </el-form-item>
          <el-form-item label="班级">
            <el-input v-model="form.clazz"></el-input>
          </el-form-item>
          <el-form-item label="性别">
            <el-input v-model="form.sex"></el-input>
          </el-form-item>
          <el-form-item label="电话号码">
            <el-input v-model="form.tel"></el-input>
          </el-form-item>
        </el-form>
      </section>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submit()">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pagination: {
        //分页后的考试信息
        current: 1, //当前页
        total: null, //记录条数
        size: 6, //每页条数
        records: []//存储学生信息
      },
      dialogVisible: false, //对话框
      form: {}, //保存点击以后当前试卷的信息
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
    this.getMajorInfo();
    this.getGradeInfo();
    this.getClazzInfo();
    
  },
  methods: {
    getClazzInfo() {//按班级查询学生信息
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
    getMajorInfo() {//按专业查询学生信息
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
    getGradeInfo() {//按年级查询学生信息
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
    // getStudentInfo() {
    //   //分页查询所有试卷信息
    //   this.$axios(`/students/${this.pagination.current}/${this.pagination.size}`).then(res => {
    //     if (res.data == 'error') {
    //       this.$message({
    //         type: 'error',
    //         message: '查询失败！'
    //       })
    //     }
    //     this.pagination.records = res.data;
    //     this.CurrentSituation = 'normal'
    //     console.log(this.pagination.records)
    //   }).catch(error => {
    //     console.log("学生信息请求失败")
    //   });
    // },
    getSpecificStudentInfo() {
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
      console.log(val)
      this.pagination.current = val;
      this.getSpecificStudentInfo();
    },
    checkGrade(studentId) { //修改学生信息
      this.dialogVisible = true
      this.$axios(`/student/${studentId}`).then(res => {
        this.form = res.data
      })
    },
    deleteById(studentId) { //删除当前学生
      this.$confirm("确定删除当前学生吗？删除后无法恢复", "Warning", {
        confirmButtonText: '确定删除',
        cancelButtonText: '算了,留着吧',
        type: 'danger'
      }).then(() => { //确认删除
        this.$axios({
          url: `/student/${studentId}`,
          method: 'DELETE',
        }).then(res => {
          this.getSpecificStudentInfo()
          if (res.data == 'ok') {
            this.$message({
              type: 'success',
              message: '删除成功！'
            })
          } else {
            this.$message({
              type: 'error',
              message: '删除失败！'
            })
          }
        }).catch(() => {
          console.log("删除请求失败")
        })
      }).catch(() => {

      })
    },
    submit() { //提交更改
      this.dialogVisible = false
      this.$axios({
        url: '/student',
        method: 'put',
        data: {
          ...this.form
        }
      }).then(res => {
        console.log(res)
        if (res.data == '200') {
          this.$message({
            message: '更新成功',
            type: 'success'
          })
        } else {
          this.$message({
            message: '操作失败',
            type: 'error'
          })
        }
        this.getSpecificStudentInfo()
      })
    },
    handleClose(done) { //关闭提醒
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        }).catch(_ => { });
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
