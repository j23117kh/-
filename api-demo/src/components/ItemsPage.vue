<template>
  <div class="container">
    <section class="form-section">
      <h3>新しい課題を追加</h3>
      <div class="form-group">
        <input v-model="formData.subject" placeholder="授業名" />
        <input v-model="formData.title" placeholder="課題名" />
        <input v-model="formData.due_date" type="date" />
        <select v-model="formData.priority">
          <option value="高">高</option>
          <option value="中">中</option>
          <option value="低">低</option>
        </select>
        <button @click="handleSave">登録</button>
      </div>
    </section>

    <hr />

    <section class="search-section">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input 
          v-model="searchQuery" 
          placeholder="授業名または課題名で検索..." 
          class="search-input"
        />
        <button v-if="searchQuery" @click="searchQuery = ''" class="clear-btn">× クリア</button>
      </div>
    </section>

    <section class="list-section">
      <h3>課題一覧</h3>
      <p class="hint">※項目名をクリックすると並び替えができます</p>
      <table class="task-table">
        <thead>
          <tr>
            <th @click="sortBy('status')" class="sortable">状態 {{ getSortIcon('status') }}</th>
            <th @click="sortBy('subject')" class="sortable">授業名 {{ getSortIcon('subject') }}</th>
            <th @click="sortBy('title')" class="sortable">課題名 {{ getSortIcon('title') }}</th>
            <th @click="sortBy('due_date')" class="sortable">期限 {{ getSortIcon('due_date') }}</th>
            <th @click="sortBy('priority')" class="sortable">優先度 {{ getSortIcon('priority') }}</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in filteredTasks" :key="task.id">
            <td>
              <span :class="['status-badge', task.status === '完了' ? 'done' : 'pending']">
                {{ task.status }}
              </span>
            </td>
            <td>
              <a @click.prevent="goToDetail(task.id)" href="#" class="item-link">
                {{ task.subject }}
              </a>
            </td>
            <td>{{ task.title }}</td>
            <td>{{ task.due_date }}</td>
            <td>{{ task.priority }}</td>
            <td>
              <button @click="goToDetail(task.id)">詳細・編集</button>
              <button @click="handleDelete(task.id)" class="btn-delete">削除</button>
            </td>
          </tr>
          <tr v-if="filteredTasks.length === 0">
            <td colspan="6" style="text-align: center; padding: 20px; color: #999;">
              一致する課題が見つかりません。
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { fetchAllItems, addItem, deleteItem } from '../api/api.js';

const tasks = ref([]);
const searchQuery = ref(''); // 🔍 検索ワードの状態管理を追加
const router = useRouter();

const formData = reactive({
  subject: '',
  title: '',
  due_date: '',
  priority: '中'
});

const sortConfig = reactive({
  key: 'due_date',
  order: 1
});

const priorityMap = { '高': 3, '中': 2, '低': 1 };

const loadTasks = async () => {
  try {
    tasks.value = await fetchAllItems();
  } catch (error) {
    console.error("データ取得失敗:", error);
  }
};

onMounted(loadTasks);

// 🔍 並び替えと検索を同時に行うように修正
const filteredTasks = computed(() => {
  // 1. まず検索ワードで絞り込む
  let result = tasks.value.filter(task => {
    const query = searchQuery.value.toLowerCase();
    return (
      task.subject.toLowerCase().includes(query) || 
      task.title.toLowerCase().includes(query)
    );
  });

  // 2. 絞り込んだ結果を並び替える
  return result.sort((a, b) => {
    let modifier = sortConfig.order;
    let valA = a[sortConfig.key];
    let valB = b[sortConfig.key];

    if (sortConfig.key === 'priority') {
      valA = priorityMap[valA] || 0;
      valB = priorityMap[valB] || 0;
    }

    if (valA < valB) return -1 * modifier;
    if (valA > valB) return 1 * modifier;
    return 0;
  });
});

const sortBy = (key) => {
  if (sortConfig.key === key) {
    sortConfig.order *= -1;
  } else {
    sortConfig.key = key;
    sortConfig.order = 1;
  }
};

const getSortIcon = (key) => {
  if (sortConfig.key !== key) return '↕️';
  return sortConfig.order === 1 ? '🔼' : '🔽';
};

const handleSave = async () => {
  if (!formData.subject || !formData.title || !formData.due_date) {
    return alert("授業名、課題名、期限をすべて入力してください");
  }
  const payload = {
    subject: formData.subject,
    title: formData.title,
    due_date: formData.due_date,
    priority: formData.priority
  };
  try {
    await addItem(payload);
    formData.subject = '';
    formData.title = '';
    formData.due_date = '';
    await loadTasks();
    alert("保存しました！");
  } catch (error) {
    alert("保存失敗: 形式を確認してください。");
  }
};

const handleDelete = async (id) => {
  if (confirm('本当に削除しますか？')) {
    await deleteItem(id);
    await loadTasks();
  }
};

const goToDetail = (id) => {
  router.push(`/items/${id}`);
};
</script>

<style scoped>
/* 既存のスタイルを維持しつつ検索窓のスタイルを追加 */
.container { padding: 20px; font-family: sans-serif; }
.form-section { background: #f4f4f4; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
.form-group { display: flex; gap: 10px; flex-wrap: wrap; }

/* 🔍 検索窓のスタイル */
.search-section { margin-bottom: 20px; text-align: left; }
.search-box { display: flex; align-items: center; gap: 10px; background: #fff; border: 1px solid #ddd; padding: 5px 15px; border-radius: 20px; width: fit-content; }
.search-input { border: none; outline: none; padding: 8px; width: 250px; font-size: 14px; }
.clear-btn { background: #eee; border: none; border-radius: 50%; width: 20px; height: 20px; cursor: pointer; font-size: 12px; display: flex; align-items: center; justify-content: center; }

.task-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.task-table th, .task-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.sortable { cursor: pointer; background-color: #eee; user-select: none; }
.sortable:hover { background-color: #ddd; }
.hint { font-size: 0.8em; color: #666; margin-bottom: 5px; }
.item-link { color: #007bff; font-weight: bold; text-decoration: none; }
.item-link:hover { text-decoration: underline; }
.btn-delete { color: white; background: #dc3545; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-left: 5px; }
.status-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.8em; }
.status-badge.done { background: #d4edda; color: #155724; }
.status-badge.pending { background: #fff3cd; color: #856404; }
</style>