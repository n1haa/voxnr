<script setup lang="ts">
import { ref, reactive } from 'vue'
import { 
  Building, 
  User, 
  Mail, 
  ShieldCheck, 
  Info, 
  BarChart3, 
  UploadCloud, 
  Sparkles, 
  Crown,
  Loader2,
  Check
} from 'lucide-vue-next'

type RoleType = 'marketer' | 'sales' | 'creator' | 'owner'

interface Company {
  id: string
  name: string
}

const authMode = ref<'login' | 'register'>('register')
const isLoading = ref<boolean>(false)

// Список привязанных/доступных компаний
const availableCompanies = ref<Company[]>([
  { id: '1', name: 'ООО "Технологии Будущего"' },
  { id: '2', name: 'ИП Смирнов (VoxNR Partner)' }
])

const form = reactive({
  companyId: '1',
  fullName: '',
  email: '',
  password: '',
  role: 'marketer' as RoleType
})

// Описание ролей и прав доступа (RBAC)
const roles = [
  {
    id: 'marketer',
    title: 'Маркетолог',
    icon: BarChart3,
    description: 'Видит аналитику (ТОП болей), ставит задачи и управляет проектами[cite: 1].'
  },
  {
    id: 'sales',
    title: 'Селз',
    icon: UploadCloud,
    description: 'Только загрузка собственных диалогов/звонков и просмотр статуса[cite: 1].'
  },
  {
    id: 'creator',
    title: 'Креатор',
    icon: Sparkles,
    description: 'Доступ к генерации контента (Reels, посты, заголовки)[cite: 1].'
  },
  {
    id: 'owner',
    title: 'Главный',
    icon: Crown,
    description: 'Полный контроль компании, биллинг и приглашения. Только 1 в системе[cite: 1].'
  }
]

const handleSubmit = () => {
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
    alert(authMode.value === 'register' 
      ? 'Запрос отправлен! Временный пароль сгенерирован и отправлен на ваш e-mail.' 
      : 'Успешный вход в систему!')
  }, 1000)
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 flex flex-col justify-center items-center p-4 md:p-8">
    <div class="max-w-2xl w-full bg-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl border border-slate-600">
      
      <!-- Шапка с переключателем режима -->
      <div class="flex justify-between items-center mb-8 border-b border-slate-600 pb-4">
        <div>
          <h1 class="text-2xl md:text-3xl font-bold text-slate-100">
            {{ authMode === 'register' ? 'Присоединиться к команде' : 'Вход в VoxNR' }}
          </h1>
          <p class="text-xs md:text-sm text-slate-400 mt-1">
            Рабочая область AI-платформы контента
          </p>
        </div>
        <div class="flex bg-slate-700 p-1 rounded-full border border-slate-600">
          <button 
            @click="authMode = 'register'" 
            :class="[
              'px-4 py-1.5 rounded-full text-xs font-medium transition-all duration-200',
              authMode === 'register' ? 'bg-gradient-to-r from-sky-400 to-purple-500 text-white shadow-md' : 'text-slate-400 hover:text-slate-100'
            ]"
          >
            Регистрация
          </button>
          <button 
            @click="authMode = 'login'" 
            :class="[
              'px-4 py-1.5 rounded-full text-xs font-medium transition-all duration-200',
              authMode === 'login' ? 'bg-gradient-to-r from-sky-400 to-purple-500 text-white shadow-md' : 'text-slate-400 hover:text-slate-100'
            ]"
          >
            Вход
          </button>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-5">
        
        <!-- Выбор компании -->
        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">Выберите организацию / Юрлицо</label>
          <div class="relative">
            <select 
              v-model="form.companyId" 
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition appearance-none pr-10"
            >
              <option v-for="comp in availableCompanies" :key="comp.id" :value="comp.id" class="bg-slate-800">
                {{ comp.name }}
              </option>
            </select>
            <Building class="w-5 h-5 text-slate-400 absolute right-3 top-3.5 pointer-events-none" />
          </div>
        </div>

        <!-- Поля ФИО и Email (для регистрации) -->
        <template v-if="authMode === 'register'">
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">ФИО сотрудника *</label>
            <div class="relative">
              <input 
                v-model="form.fullName" 
                type="text" 
                placeholder="Сергей Алексеев"
                required
                class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 pl-11 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
              />
              <User class="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Рабочий e-mail *</label>
            <div class="relative">
              <input 
                v-model="form.email" 
                type="email" 
                placeholder="s.alekseev@company.com"
                required
                class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 pl-11 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
              />
              <Mail class="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
            </div>
          </div>

          <!-- Выбор роли (RBAC) -->
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-2">Назначаемая роль</label>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div 
                v-for="role in roles" 
                :key="role.id"
                @click="form.role = role.id as RoleType"
                :class="[
                  'p-4 rounded-xl border cursor-pointer transition-all duration-200 relative flex flex-col justify-between',
                  form.role === role.id 
                    ? 'border-sky-400 bg-slate-700/80 shadow-md shadow-sky-400/10' 
                    : 'border-slate-600 bg-slate-700/30 hover:bg-slate-700/50'
                ]"
              >
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2 font-medium text-slate-100 text-sm">
                    <component :is="role.icon" class="w-4 h-4 text-sky-400" />
                    {{ role.title }}
                  </div>
                  <span v-if="form.role === role.id" class="w-4 h-4 bg-sky-400 text-slate-900 rounded-full flex items-center justify-center">
                    <Check class="w-3 h-3 stroke-[3]" />
                  </span>
                </div>
                <p class="text-xs text-slate-400 leading-relaxed">{{ role.description }}</p>
              </div>
            </div>
          </div>

          <!-- Инфо-пашка про пароль -->
          <div class="p-3 bg-sky-400/10 border border-sky-400/30 rounded-xl flex items-start gap-3">
            <Info class="w-5 h-5 text-sky-400 shrink-0 mt-0.5" />
            <p class="text-xs text-slate-300">
              Пароль генерируется автоматически алгоритмом защиты VoxNR и сразу высылается на указанный e-mail.
            </p>
          </div>
        </template>

        <!-- Поля для обычного входа -->
        <template v-else>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">E-mail</label>
            <input 
              v-model="form.email" 
              type="email" 
              placeholder="user@company.com"
              required
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">Пароль из письма</label>
            <input 
              v-model="form.password" 
              type="password" 
              placeholder="••••••••••••"
              required
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
          </div>
        </template>

        <!-- Кнопка действия -->
        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full mt-4 bg-gradient-to-r from-sky-400 to-purple-500 text-white font-medium rounded-full px-6 py-3 shadow-md shadow-sky-400/25 hover:scale-[1.02] hover:shadow-lg transition-all duration-200 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
          <span>{{ authMode === 'register' ? 'Запросить доступ и пароль' : 'Войти в рабочую область' }}</span>
        </button>

      </form>
    </div>
  </div>
</template>