<template>
    <section class="profile">
        <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="姓名">
                <el-input v-model="form.teacherName" :disabled="!isEditing"></el-input>
            </el-form-item>
            <el-form-item label="学院">
                <el-input v-model="form.institute" :disabled="!isEditing"></el-input>
            </el-form-item>
            <el-form-item label="性别">
                <el-input v-model="form.sex" :disabled="!isEditing"></el-input>
            </el-form-item>
            <el-form-item label="电话号码">
                <el-input v-model="form.tel" :disabled="!isEditing"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
                <el-input v-model="form.email" :disabled="!isEditing"></el-input>
            </el-form-item>
            <el-form-item label="密码" v-if="isEditing">
                <el-input v-model="form.pwd"></el-input>
            </el-form-item>
            <el-form-item label="身份证号">
                <el-input v-model="form.cardId" :disabled="!isEditing"></el-input>
            </el-form-item>
            <el-form-item label="职称">
                <el-input v-model="form.type" :disabled="!isEditing"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button v-if="!isEditing" type="primary" @click="startEditing">编辑</el-button>
                <el-button v-else type="primary" @click="saveProfile">保存</el-button>
                <el-button type="text" @click="cancelEdit" v-if="isEditing">取消</el-button>
            </el-form-item>
        </el-form>
    </section>
</template>

  
<script>
import VueCookies from 'vue-cookies';
export default {
    data() {
        return {
            form: {
            }, // 教师个人信息
            isEditing: false // 是否处于编辑状态
        };
    },
    created() {
        this.fetchTeacherProfile(); // 在组件创建时获取当前教师信息
    },
    methods: {
        fetchTeacherProfile() {
            const teacherId = VueCookies.get("cid");

            if (teacherId) {
                this.$axios({
                    url: `/seacherteacher/${teacherId}`,
                    method: 'get'
                }).then(res => {
                    if (res.data.code === 200) {
                        // 更新表单数据
                        this.form = res.data.data.records;
                    } else {
                        this.$message.error('获取教师信息失败');
                    }
                }).catch(error => {
                    console.error('获取教师信息失败:', error);
                    this.$message.error('获取教师信息失败');
                });
            } else {
                // 处理教师ID不可用的情况
                console.error('无法获取教师ID');
                this.$message.error('无法获取教师信息，教师ID未提供');
            }
        },saveProfile() {
            this.$axios({
                url: '/teacher/edit',
                method: 'post',
                data: {
                    ...this.form
                }
            }).then(res => {
                if (res.data.code == 200) {
                    this.isEditing = false;
                    this.$message.success('修改成功');
                } else {
                    this.$message.error('修改失败');
                }
            }
            )
        }, startEditing() {
            this.isEditing = true;
        }, cancelEdit() {
            // 在取消编辑时，重新获取个人信息，以取消可能的修改
            this.fetchTeacherProfile();
            this.isEditing = false;
        }
    },
};
</script>
  
<style lang="less" scoped>
.edit-profile {
    padding: 0px 40px;
    width: 400px;
}
</style>
  

<style lang="less" scoped>
.profile {
    padding: 0px 40px;
    width: 400px;
}
</style>