<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { 
  User, 
  Mail, 
  Lock, 
  CheckCircle2, 
  ArrowRight, 
  ArrowLeft, 
  Loader2,
  Search
} from 'lucide-vue-next'

// Состояние шагов (1 - Юр. лицо, 2 - Аккаунт Owner, 3 - Готово)
const currentStep = ref<number>(1)
const isDebouncing = ref<boolean>(false)
const isSubmitting = ref<boolean>(false)

const form = reactive({
  inn: '',
  companyName: '',
  kpp: '',
  ogrn: '',
  address: '',
  fullName: '',
  email: '',
  password: ''
})

// Прогресс заполнения в процентах
const progressPercentage = computed(() => {
  if (currentStep.value === 1) return 33
  if (currentStep.value === 2) return 66
  return 100
})

// Имитация поиска по ИНН (Dadata/ФНС)
let debounceTimer: ReturnType<typeof setTimeout> | null = null
const handleInnInput = () => {
  if (form.inn.length < 10) return
  isDebouncing.value = true
  
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    // Имитация ответа API Dadata
    if (form.inn === '7707083893') {
      form.companyName = 'ООО "ТЕХНОЛОГИИ БУДУЩЕГО"'
      form.kpp = '773601001'
      form.ogrn = '1027700132195'
      form.address = 'г. Москва, ул. Покровка, д. 10, стр. 1'
    } else {
      form.companyName = 'ООО "ВОКСНР СОФТВЕЙР"'
      form.kpp = '616401001'
      form.ogrn = '1236100004567'
      form.address = 'г. Ростов-на-Дону, ул. Большая Садовая, д. 105'
    }
    isDebouncing.value = false
  }, 600)
}

const handleNextStep = () => {
  if (currentStep.value === 1 && form.inn && form.companyName) {
    currentStep.value = 2
  }
}

const handleRegisterCompany = async () => {
  isSubmitting.value = true
  // Имитация отправки POST /api/v1/auth/register-company
  setTimeout(() => {
    isSubmitting.value = false
    currentStep.value = 3
  }, 1200)
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 flex flex-col justify-center items-center p-4 md:p-8">
    <div class="max-w-xl w-full bg-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl border border-slate-600">
      
      <!-- Заголовок -->
      <div class="text-center mb-6">
        <h1 class="text-3xl md:text-4xl font-bold leading-tight text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-purple-500 mb-2">
          VoxNR
        </h1>
        <p class="text-slate-400 text-sm md:text-base">
          Регистрация компании и создание аккаунта Владельца
        </p>
      </div>

      <!-- Прогресс-бар -->
      <div class="mb-8">
        <div class="flex justify-between text-xs text-slate-400 mb-2 font-medium">
          <span>Шаг {{ currentStep }} из 3</span>
          <span>{{ progressPercentage }}% заполнено</span>
        </div>
        <div class="w-full h-2 bg-slate-600 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-sky-400 to-purple-500 rounded-full transition-all duration-700 ease-out"
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>
      </div>

      <!-- ШАГ 1: Реквизиты компании -->
      <form v-if="currentStep === 1" @submit.prevent="handleNextStep" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">ИНН организации *</label>
          <div class="relative">
            <input 
              v-model="form.inn" 
              @input="handleInnInput"
              type="text" 
              maxlength="12"
              placeholder="Введите 10 или 12 цифр ИНН"
              required
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 pl-11 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
            <Search class="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
            <Loader2 v-if="isDebouncing" class="w-5 h-5 text-sky-400 absolute right-3 top-3.5 animate-spin" />
          </div>
          <span class="text-xs text-slate-400 mt-1 block">Автозаполнение данных через ФНС / Dadata</span>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">Наименование компании</label>
          <input 
            v-model="form.companyName" 
            type="text" 
            placeholder="Заполнится автоматически"
            required
            class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">КПП</label>
            <input 
              v-model="form.kpp" 
              type="text" 
              placeholder="КПП"
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-400 mb-1">ОГРН / ОГРНИП</label>
            <input 
              v-model="form.ogrn" 
              type="text" 
              placeholder="ОГРН"
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">Юридический адрес</label>
          <input 
            v-model="form.address" 
            type="text" 
            placeholder="Адрес компании"
            class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
          />
        </div>

        <button 
          type="submit" 
          :disabled="!form.companyName"
          class="w-full mt-6 bg-gradient-to-r from-sky-400 to-purple-500 text-white font-medium rounded-full px-6 py-3 shadow-md shadow-sky-400/25 hover:scale-[1.02] hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:hover:scale-100 flex items-center justify-center gap-2"
        >
          Далее: Данные администратора
          <ArrowRight class="w-5 h-5" />
        </button>
      </form>

      <!-- ШАГ 2: Данные Главного (Owner) -->
      <form v-else-if="currentStep === 2" @submit.prevent="handleRegisterCompany" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">ФИО Администратора (Главный)</label>
          <div class="relative">
            <input 
              v-model="form.fullName" 
              type="text" 
              placeholder="Иванов Иван Иванович"
              required
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 pl-11 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
            <User class="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">Рабочий E-mail</label>
          <div class="relative">
            <input 
              v-model="form.email" 
              type="email" 
              placeholder="admin@company.com"
              required
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 pl-11 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
            <Mail class="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-400 mb-1">Пароль</label>
          <div class="relative">
            <input 
              v-model="form.password" 
              type="password" 
              placeholder="••••••••••••"
              required
              class="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 pl-11 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent transition"
            />
            <Lock class="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
          </div>
        </div>

        <div class="flex gap-3 pt-4">
          <button 
            type="button" 
            @click="currentStep = 1"
            class="border border-sky-400 text-sky-400 bg-transparent rounded-full px-6 py-3 hover:bg-sky-400/10 transition flex items-center justify-center gap-2"
          >
            <ArrowLeft class="w-5 h-5" />
            Назад
          </button>
          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="flex-1 bg-gradient-to-r from-sky-400 to-purple-500 text-white font-medium rounded-full px-6 py-3 shadow-md shadow-sky-400/25 hover:scale-[1.02] transition-all duration-200 flex items-center justify-center gap-2"
          >
            <Loader2 v-if="isSubmitting" class="w-5 h-5 animate-spin" />
            <span>Зарегистрировать компанию</span>
          </button>
        </div>
      </form>

      <!-- ШАГ 3: Успешное подтверждение -->
      <div v-else class="text-center py-6 space-y-4 animate-fade-in-up">
        <div class="w-16 h-16 bg-green-400/20 text-green-400 rounded-full flex items-center justify-center mx-auto">
          <CheckCircle2 class="w-10 h-10" />
        </div>
        <h2 class="text-2xl font-bold text-slate-100">Компания успешно зарегистрирована!</h2>
        <p class="text-slate-400 text-sm">
          Мы отправили письмо с подтверждением на <span class="text-sky-400 font-medium">{{ form.email }}</span>. Перейдите по ссылке в письме для активации.
        </p>
      </div>

    </div>
  </div>
</template>