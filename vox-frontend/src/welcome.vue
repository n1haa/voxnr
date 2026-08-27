<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Sparkles, 
  ArrowRight, 
  Play, 
  Building2, 
  Users, 
  LayoutDashboard, 
  UploadCloud, 
  Wand2, 
  BarChart2, 
  Zap, 
  CheckCircle2, 
  Menu,
  X,
} from 'lucide-vue-next'

// Состояние мобильного меню
const isMobileMenuOpen = ref<boolean>(false)
const router = useRouter()

// Данные для навигатора по экранам (Быстрый переход к созданным модулям)
const appScreens = [
  {
    id: 1,
    title: 'Welcome-страница',
    subtitle: 'Главный лендинг и карточка УТП',
    icon: Sparkles,
    badge: 'Текущий экран',
    badgeStyle: 'bg-sky-400/20 text-sky-400',
    routeName: 'welcome',
    active: true
  },
  {
    id: 2,
    title: 'Регистрация компании',
    subtitle: 'Экран №2. Ввод ИНН, ФНС-автозаполнение, Owner',
    icon: Building2,
    badge: 'Экран №2 (ТЗ)',
    badgeStyle: 'bg-green-400/20 text-green-400',
    routeName: 'register-company',
    active: true
  },
  {
    id: 3,
    title: 'Вход / Инвайт сотрудника',
    subtitle: 'Выбор юрлица, RBAC ролей (Маркетолог, Селз, Креатор)',
    icon: Users,
    badge: 'Спец-экран',
    badgeStyle: 'bg-purple-500/20 text-purple-400',
    routeName: 'employee-auth',
    active: true
  },
  {
    id: 4,
    title: 'Дашборд проектов',
    subtitle: 'Карточки проектов, счетчик 10+ диалогов, статусы',
    icon: LayoutDashboard,
    badge: 'В разработке',
    badgeStyle: 'bg-slate-700 text-slate-400',
    routeName: 'dashboard',
    active: false
  },
  {
    id: 5,
    title: 'Загрузка данных',
    subtitle: 'Drag-and-Drop аудио/текста, тумблер типа лида',
    icon: UploadCloud,
    badge: 'В разработке',
    badgeStyle: 'bg-slate-700 text-slate-400',
    routeName: 'upload',
    active: false
  },
  {
    id: 6,
    title: 'SMM-Центр & AI Генерация',
    subtitle: 'Split-Screen: ТОП болей, генератор сценариев Reels/постов',
    icon: Wand2,
    badge: 'В разработке',
    badgeStyle: 'bg-slate-700 text-slate-400',
    routeName: 'smm-center',
    active: false
  }
]

// Визуальный процесс работы VoxNR Pipeline
const pipelineSteps = [
  {
    step: '01',
    title: 'Загрузка звонков',
    desc: 'Загрузите аудио MP3/WAV или текстовые переписки менеджеров и CustDev.',
    icon: UploadCloud
  },
  {
    step: '02',
    title: 'STT & Qwen AI Analysis',
    desc: 'Whisper транскрибирует аудио, а Qwen извлекает дословные боли и сленг ЦА.',
    icon: Zap
  },
  {
    step: '03',
    title: 'Кластеризация инсайтов',
    desc: 'При 10+ диалогах формируется ТОП-5 сквозных проблем с эмоциональным накалом.',
    icon: BarChart2
  },
  {
    step: '04',
    title: 'One-Click Генератор',
    desc: 'Создание постов, цепляющих заголовков и сценариев для Reels/TikTok.',
    icon: Sparkles
  }
]

// Переход к экрану (Имитация Vue Router)
const navigateTo = (routeName: string, isActive = true) => {
  if (isActive) {
    router.push({ name: routeName })
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 font-sans selection:bg-sky-400 selection:text-slate-900">
    
    <!-- ========================================== -->
    <!-- 1. КРАСИВАЯ ШАПКА (HEADER)                 -->
    <!-- ========================================== -->
    <header class="sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-600 transition-all">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        <!-- Логотип -->
        <div class="flex items-center gap-3 cursor-pointer" @click="navigateTo('welcome')">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-400 to-purple-500 flex items-center justify-center shadow-lg shadow-sky-400/20">
            <Sparkles class="w-6 h-6 text-white" />
          </div>
          <div class="flex flex-col">
            <span class="text-2xl font-bold tracking-tight text-white flex items-center gap-1.5">
              VoxNR
              <span class="text-xs px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-400 font-semibold border border-purple-500/30">MVP</span>
            </span>
            <span class="text-[10px] text-slate-400 font-medium tracking-wide uppercase">AI Content Intelligence</span>
          </div>
        </div>

        <!-- Навигационные ссылки (Desktop) -->
        <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
          <a href="#navigator" class="hover:text-sky-400 transition-colors">Экраны MVP</a>
          <a href="#features" class="hover:text-sky-400 transition-colors">Возможности</a>
          <a href="#pipeline" class="hover:text-sky-400 transition-colors">Как это работает</a>
          <a href="#comparison" class="hover:text-sky-400 transition-colors">Преимущества</a>
        </nav>

        <!-- Кнопки действия (Desktop) -->
        <div class="hidden md:flex items-center gap-4">
          <button 
            @click="navigateTo('employee-auth')" 
            class="text-sm font-medium text-slate-300 hover:text-white px-4 py-2 transition"
          >
            Войти сотруднику
          </button>
          
          <button 
            @click="navigateTo('register-company')" 
            class="bg-gradient-to-r from-sky-400 to-purple-500 text-white font-medium rounded-full px-5 py-2.5 text-sm shadow-md shadow-sky-400/20 hover:scale-105 hover:shadow-lg transition-all duration-200 flex items-center gap-2"
          >
            <span>Начать анализ</span>
            <ArrowRight class="w-4 h-4" />
          </button>
        </div>

        <!-- Мобильная кнопка бургера -->
        <div class="flex md:hidden">
          <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="text-slate-400 hover:text-white p-2">
            <Menu v-if="!isMobileMenuOpen" class="w-6 h-6" />
            <X v-else class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- Выпадающее меню (Mobile) -->
      <div v-if="isMobileMenuOpen" class="md:hidden bg-slate-800 border-b border-slate-600 px-4 pt-2 pb-6 space-y-3 animate-fade-in-up">
        <a href="#navigator" @click="isMobileMenuOpen = false" class="block text-slate-300 hover:text-sky-400 py-2">Экраны MVP</a>
        <a href="#features" @click="isMobileMenuOpen = false" class="block text-slate-300 hover:text-sky-400 py-2">Возможности</a>
        <a href="#pipeline" @click="isMobileMenuOpen = false" class="block text-slate-300 hover:text-sky-400 py-2">Как это работает</a>
        <div class="pt-4 border-t border-slate-700 flex flex-col gap-3">
          <button 
            @click="navigateTo('employee-auth')" 
            class="w-full border border-sky-400 text-sky-400 rounded-full px-4 py-2.5 text-sm font-medium text-center"
          >
            Войти сотруднику
          </button>
          <button 
            @click="navigateTo('register-company')" 
            class="w-full bg-gradient-to-r from-sky-400 to-purple-500 text-white rounded-full px-4 py-2.5 text-sm font-medium text-center"
          >
            Регистрация компании
          </button>
        </div>
      </div>
    </header>

    <!-- ========================================== -->
    <!-- 2. HERO-СЕКЦИЯ                             -->
    <!-- ========================================== -->
    <section class="relative py-16 md:py-24 overflow-hidden">
      <!-- Фоновый декоративный свечение -->
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-sky-500/15 to-purple-500/15 blur-[120px] rounded-full pointer-events-none"></div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        
        <!-- Бейдж -->
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-800 border border-slate-600 text-xs md:text-sm font-medium text-sky-400 mb-6 shadow-lg">
          <Zap class="w-4 h-4 text-yellow-400" />
          <span>Умная контент-аналитика для B2B и SMM-команд</span>
        </div>

        <!-- Главный заголовок H1 -->
        <h1 class="text-4xl md:text-6xl font-bold text-slate-100 leading-tight tracking-tight max-w-4xl mx-auto mb-6">
          Превратите разговоры с клиентами в 
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-purple-500">
            готовый продающий контент
          </span>
        </h1>

        <!-- Подзаголовок -->
        <p class="text-slate-400 text-base md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
          VoxNR автоматически анализирует аудиозаписи звонков и переписки, находить точные боли и формулировки ЦА, сразу генерируя посты, заголовки и сценарии для Reels/TikTok.
        </p>

        <!-- CTA Кнопки -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <button 
            @click="navigateTo('register-company')" 
            class="w-full sm:w-auto bg-gradient-to-r from-sky-400 to-purple-500 text-white font-semibold rounded-full px-8 py-4 shadow-xl shadow-sky-400/25 hover:scale-105 hover:shadow-2xl transition-all duration-200 flex items-center justify-center gap-3 text-base"
          >
            <span>Создать аккаунт компании</span>
            <ArrowRight class="w-5 h-5" />
          </button>
          
          <a 
            href="#navigator" 
            class="w-full sm:w-auto border border-sky-400 text-sky-400 hover:bg-sky-400/10 font-medium rounded-full px-8 py-4 transition-all duration-200 flex items-center justify-center gap-2 text-base"
          >
            <Play class="w-4 h-4 fill-current" />
            <span>Обзор экранов системы</span>
          </a>
        </div>

        <!-- Метрики над доверием -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto pt-8 border-t border-slate-800">
          <div class="p-4 bg-slate-800/50 rounded-2xl border border-slate-700/50">
            <div class="text-2xl md:text-3xl font-bold text-sky-400 mb-1">в 3 раза</div>
            <div class="text-xs text-slate-400">Быстрее создание контент-плана</div>
          </div>
          <div class="p-4 bg-slate-800/50 rounded-2xl border border-slate-700/50">
            <div class="text-2xl md:text-3xl font-bold text-purple-400 mb-1">100%</div>
            <div class="text-xs text-slate-400">Язык и дословные цитаты ЦА</div>
          </div>
          <div class="p-4 bg-slate-800/50 rounded-2xl border border-slate-700/50">
            <div class="text-2xl md:text-3xl font-bold text-green-400 mb-1">10+</div>
            <div class="text-xs text-slate-400">Звонков для ТОП-инсайтов</div>
          </div>
          <div class="p-4 bg-slate-800/50 rounded-2xl border border-slate-700/50">
            <div class="text-2xl md:text-3xl font-bold text-yellow-400 mb-1">Qwen AI</div>
            <div class="text-xs text-slate-400">Локальный LLM & STT пайплайн</div>
          </div>
        </div>

      </div>
    </section>

    <!-- ========================================== -->
    <!-- 3. НАВИГАТОР ПО ВСЕМ ЭКРАНАМ СИСТЕМЫ       -->
    <!-- ========================================== -->
    <section id="navigator" class="py-16 bg-slate-800/40 border-y border-slate-700/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-slate-100 mb-3">Быстрый переход по экранам VoxNR</h2>
          <p class="text-slate-400 text-base max-w-xl mx-auto">
            Используйте эту панель для навигации между всеми спроектированными модулями и экранами приложения.
          </p>
        </div>

        <!-- Сетка карточек экранов -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="screen in appScreens" 
            :key="screen.id"
            @click="navigateTo(screen.routeName, screen.active)"
            class="bg-slate-800 rounded-2xl p-6 shadow-lg border border-slate-600/70 hover:border-sky-400 transition-all duration-200 hover:-translate-y-1 cursor-pointer flex flex-col justify-between group"
          >
            <div>
              <div class="flex items-center justify-between mb-4">
                <div class="w-12 h-12 rounded-xl bg-slate-700 flex items-center justify-center text-sky-400 group-hover:bg-sky-400 group-hover:text-slate-900 transition-colors">
                  <component :is="screen.icon" class="w-6 h-6" />
                </div>
                <span :class="['px-3 py-1 rounded-full text-xs font-medium', screen.badgeStyle]">
                  {{ screen.badge }}
                </span>
              </div>
              
              <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-sky-400 transition-colors">
                {{ screen.title }}
              </h3>
              <p class="text-sm text-slate-400 leading-relaxed mb-6">
                {{ screen.subtitle }}
              </p>
            </div>

            <div class="flex items-center text-sm font-medium text-sky-400 gap-1 group-hover:gap-2 transition-all">
              <span>Открыть экран</span>
              <ArrowRight class="w-4 h-4" />
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ========================================== -->
    <!-- 4. ВИЗУАЛЬНАЯ СХЕМА РАБОТЫ (PIPELINE)      -->
    <!-- ========================================== -->
    <section id="pipeline" class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-slate-100 mb-4">Как VoxNR превращает данные в контент</h2>
          <p class="text-slate-400 text-base max-w-2xl mx-auto">
            Автоматизированный процесс от первичного аудиозаписи до готовых маркетинг-активов в 4 простых шага.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div 
            v-for="item in pipelineSteps" 
            :key="item.step"
            class="bg-slate-800 rounded-2xl p-6 shadow-lg border border-slate-700 relative overflow-hidden"
          >
            <div class="text-5xl font-extrabold text-slate-700/40 absolute top-3 right-4 select-none">
              {{ item.step }}
            </div>
            <div class="w-10 h-10 rounded-xl bg-sky-400/10 text-sky-400 flex items-center justify-center mb-4">
              <component :is="item.icon" class="w-5 h-5" />
            </div>
            <h3 class="text-lg font-bold text-slate-100 mb-2">{{ item.title }}</h3>
            <p class="text-sm text-slate-400 leading-relaxed">{{ item.desc }}</p>
          </div>
        </div>

      </div>
    </section>

    <!-- ========================================== -->
    <!-- 5. СРАВНЕНИЕ (BEFORE / AFTER)              -->
    <!-- ========================================== -->
    <section id="comparison" class="py-16 bg-slate-800/30 border-t border-slate-700">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-slate-100 mb-3">Забудьте про ручные CustDev таблицы</h2>
          <p class="text-slate-400 text-sm md:text-base">Сравнение классического подхода и AI-платформы VoxNR</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Ручной подход -->
          <div class="bg-slate-800/80 rounded-2xl p-6 border border-slate-700">
            <h3 class="text-xl font-bold text-red-400 mb-4 flex items-center gap-2">
              <span>Ручной анализ и интуиция</span>
            </h3>
            <ul class="space-y-3 text-sm text-slate-400">
              <li class="flex items-start gap-2">
                <span class="text-red-400 font-bold">✕</span>
                10–15 часов ручной расшифровки звонков и сведений в Excel
              </li>
              <li class="flex items-start gap-2">
                <span class="text-red-400 font-bold">✕</span>
                Темы постов берутся «из головы» или копируются у конкурентов
              </li>
              <li class="flex items-start gap-2">
                <span class="text-red-400 font-bold">✕</span>
                Слабая конверсия: текст напичкан сложными академическими словами
              </li>
            </ul>
          </div>

          <!-- VoxNR AI -->
          <div class="bg-slate-800 rounded-2xl p-6 border border-sky-400/50 shadow-lg shadow-sky-400/5">
            <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center gap-2">
              <Sparkles class="w-5 h-5" />
              <span>VoxNR (AI-Аналитика)</span>
            </h3>
            <ul class="space-y-3 text-sm text-slate-300">
              <li class="flex items-start gap-2">
                <CheckCircle2 class="w-5 h-5 text-green-400 shrink-0" />
                0 часов на рутину: загрузка записей в 1 клик
              </li>
              <li class="flex items-start gap-2">
                <CheckCircle2 class="w-5 h-5 text-green-400 shrink-0" />
                Точное попадание: выявление ТОП болей из real-data
              </li>
              <li class="flex items-start gap-2">
                <CheckCircle2 class="w-5 h-5 text-green-400 shrink-0" />
                100% сохранение сленга и точных цитат клиентов
              </li>
            </ul>
          </div>
        </div>

      </div>
    </section>

    <!-- ========================================== -->
    <!-- 6. FOOTER (ПОДВАЛ)                         -->
    <!-- ========================================== -->
    <footer class="bg-slate-950 border-t border-slate-800 py-12 text-slate-400 text-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-sky-400 to-purple-500 flex items-center justify-center text-white">
            <Sparkles class="w-4 h-4" />
          </div>
          <span class="font-bold text-slate-100 text-lg">VoxNR</span>
        </div>
        <div class="text-center md:text-left text-xs text-slate-500">
          © 2026 VoxNR AI Platform. Все права защищены. Python FastAPI / Vue.js 3 / Qwen LLM.
        </div>
        <div class="flex gap-6 text-xs text-slate-400">
          <a href="#" class="hover:text-sky-400 transition">Политика конфиденциальности</a>
          <a href="#" class="hover:text-sky-400 transition">Безопасность (AES-256)</a>
        </div>
      </div>
    </footer>

  </div>
</template>