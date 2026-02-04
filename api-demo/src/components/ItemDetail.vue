<template>
  <div class="container">
    <h2>課題の詳細・編集</h2>

    <p v-if="loading">読み込み中...</p>
    <p v-if="error" style="color:red;">{{ error }}</p>

    <div v-if="item" class="edit-form">
      <p><strong>管理ID:</strong> {{ item.id }}</p>

      <div class="form-item">
        <label>状態:</label>
        <select v-model="item.status" :class="taskStatusClass">
          <option value="未完了">未完了</option>
          <option value="完了">完了</option>
        </select>
      </div>

      <div class="form-item">
        <label>授業名:</label>
        <input v-model="item.subject" />
      </div>

      <div class="form-item">
        <label>課題名:</label>
        <input v-model="item.title" />
      </div>

      <div class="form-item">
        <label>期限:</label>
        <input v-model="item.due_date" type="date" />
      </div>

      <div class="form-item">
        <label>優先度:</label>
        <select v-model="item.priority">
          <option value="高">高</option>
          <option value="中">中</option>
          <option value="低">低</option>
        </select>
      </div>

      <div class="button-group">
        <button @click="onUpdate" :disabled="submitting" class="btn-update">
          {{ submitting ? "更新中..." : "変更を保存" }}
        </button>

        <button @click="onDelete" :disabled="submitting" class="btn-delete">
          削除
        </button>
      </div>
    </div>

    <p style="margin-top:16px;">
      <RouterLink to="/">← 一覧へ戻る</RouterLink>
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchItem, updateItem, deleteItem } from "../api/api.js";

const route = useRoute();
const router = useRouter();

const item = ref(null);
const loading = ref(true);
const submitting = ref(false);
const error = ref("");

// 状態に応じてクラスを切り替え
const taskStatusClass = computed(() => {
  return item.value?.status === '完了' ? 'status-done' : 'status-pending';
});

onMounted(async () => {
  try {
    const data = await fetchItem(route.params.id);
    item.value = data;
  } catch (e) {
    error.value = `取得に失敗：${e.message}`;
  } finally {
    loading.value = false;
  }
});

const onUpdate = async () => {
  submitting.value = true;
  try {
    // 全てのフィールドをバックエンドに送信する
    await updateItem(item.value.id, {
      subject: item.value.subject,
      title: item.value.title,
      due_date: item.value.due_date,
      priority: item.value.priority,
      status: item.value.status // ここで「完了」がDBに保存される
    });
    alert("更新しました");
    router.push("/"); // 更新後、一覧に戻る
  } catch (e) {
    error.value = `更新に失敗：${e.message}`;
  } finally {
    submitting.value = false;
  }
};

const onDelete = async () => {
  if (!confirm("本当に削除してよいですか？")) return;
  submitting.value = true;
  try {
    await deleteItem(item.value.id);
    alert("削除しました");
    router.push("/");
  } catch (e) {
    error.value = `削除に失敗：${e.message}`;
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.container { padding: 20px; max-width: 600px; margin: 0 auto; }
.edit-form { text-align: left; background: #f9f9f9; padding: 20px; border-radius: 8px; }
.form-item { margin-bottom: 15px; }
.form-item label { display: block; font-weight: bold; margin-bottom: 5px; }
.form-item input, .form-item select { width: 100%; padding: 8px; box-sizing: border-box; }
.button-group { margin-top: 20px; display: flex; gap: 10px; }
.btn-update { background-color: #28a745; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; }
.btn-delete { background-color: #dc3545; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; }
.status-done { border-left: 5px solid #28a745; }
.status-pending { border-left: 5px solid #ffc107; }
</style>