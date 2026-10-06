# -*- coding: utf-8 -*-
"""
Сайт-шутка для друзей.
Запуск: python сайт.py
Открыть в браузере: http://127.0.0.1:5000

Если Flask не установлен:
    pip install flask
"""

from flask import Flask, render_template_string, request, session
import random

app = Flask(__name__)
app.secret_key = "super-secret-joke-key-change-me"  # нужен для session


# ============================================================
# 30 ВОПРОСОВ  (меняй текст здесь)
# ============================================================
QUESTIONS = [
    ("Как я скорее всего проведу свободный вечер?", [
        "Дома, в тишине, с фильмом или книгой",
        "С друзьями где-то в городе",
        "За компьютером/играми/сериалом",
        "Пойду куда-нибудь один(а) — погулять или в кафе",
    ]),
    ("Что я выберу, если нужно поесть вне дома?", [
        "Что-то привычное и проверенное",
        "Что-то новое, что ещё не пробовал(а)",
        "Фастфуд, потому что быстро",
        "Кофе и десерт вместо еды",
    ]),
    ("Как я реагирую на конфликт?", [
        "Стараюсь сразу всё обсудить",
        "Замыкаюсь и перевариваю внутри",
        "Отшучиваюсь, чтобы разрядить обстановку",
        "Мне нужно время, потом вернусь к разговору",
    ]),
    ("Что для меня важнее в дружбе?", [
        "Чтобы можно было молчать вместе",
        "Чтобы всегда могли поговорить по душам",
        "Чтобы было весело и легко",
        "Чтобы можно было положиться в трудный момент",
    ]),
    ("Как я отношусь к спонтанным планам?", [
        "Люблю — чем неожиданнее, тем лучше",
        "Нормально, если не срывает другие дела",
        "Не люблю, мне нужно время подготовиться",
        "Зависит от настроения и компании",
    ]),
    ("Что меня больше всего выбивает из колеи?", [
        "Когда меня не слушают",
        "Когда нарушают мои планы",
        "Когда меня несправедливо критикуют",
        "Когда вокруг шум и суета",
    ]),
    ("Как я обычно принимаю важные решения?", [
        "Долго взвешиваю всё",
        "Полагаюсь на интуицию",
        "Советуюсь с близкими",
        "Решаю быстро и потом не жалею",
    ]),
    ("Что я делаю, когда мне плохо?", [
        "Пишу/звоню другу",
        "Ухожу в себя",
        "Отвлекаюсь работой или хобби",
        "Иду гулять или занимаюсь спортом",
    ]),
    ("Какая черта характера у меня самая заметная?", [
        "Спокойствие",
        "Эмоциональность",
        "Чувство юмора",
        "Упрямство",
    ]),
    ("Что я ценю в людях больше всего?", [
        "Честность",
        "Доброту",
        "Надёжность",
        "Умение поддержать",
    ]),
    ("Как я отношусь к большим компаниям?", [
        "Люблю, чем больше людей, тем лучше",
        "Нормально, если это близкие люди",
        "Предпочитаю 2–3 человека",
        "Избегаю, если можно",
    ]),
    ("Что я скорее выберу на выходные?", [
        "Поездку куда-нибудь",
        "Полный отдых дома",
        "Встречу с друзьями",
        "Занятие своим хобби",
    ]),
    ("Как я веду себя, когда опаздываю?", [
        "Извиняюсь и переживаю",
        "Шучу, чтобы сгладить",
        "Не придаю значения",
        "Стараюсь вообще не опаздывать",
    ]),
    ("Что для меня самый большой комплимент?", [
        "«С тобой легко»",
        "«Тебе можно доверять»",
        "«Ты очень интересный человек»",
        "«Ты добрый(ая)»",
    ]),
    ("Как я реагирую на критику?", [
        "Спокойно, если по делу",
        "Болезненно, даже если по делу",
        "Могу поспорить",
        "Зависит от того, кто критикует",
    ]),
    ("Что я делаю, если друг просит о помощи?", [
        "Помогу, даже если неудобно",
        "Помогу, если это в моих силах",
        "Сначала спрошу, что именно нужно",
        "Могу отказать, если это мне не подходит",
    ]),
    ("Какой у меня стиль в одежде?", [
        "Удобство важнее всего",
        "Что-то нейтральное и аккуратное",
        "Люблю выделяться",
        "Зависит от настроения",
    ]),
    ("Что я обычно делаю в дороге?", [
        "Слушаю музыку",
        "Смотрю в окно и думаю",
        "Читаю или листаю телефон",
        "Разговариваю с попутчиками",
    ]),
    ("Как я отношусь к неожиданным подаркам?", [
        "Очень радуюсь",
        "Немного смущаюсь",
        "Люблю, когда дарят что-то нужное",
        "Предпочитаю выбирать сам(а)",
    ]),
    ("Что для меня идеальный отдых?", [
        "Море и солнце",
        "Горы и природа",
        "Город и новые места",
        "Дом и тишина",
    ]),
    ("Как я обычно выражаю симпатию?", [
        "Словами",
        "Делами",
        "Вниманием и заботой",
        "Временем, которое провожу с человеком",
    ]),
    ("Что меня радует больше всего?", [
        "Когда планы сбываются",
        "Когда близкие рядом",
        "Когда узнаю что-то новое",
        "Когда есть время на себя",
    ]),
    ("Как я отношусь к переменам?", [
        "Люблю, когда жизнь меняется",
        "Принимаю, если нужно",
        "Предпочитаю стабильность",
        "Боюсь, но иду вперёд",
    ]),
    ("Что я делаю, если мы поссорились?", [
        "Первым(ой) иду на контакт",
        "Жду, пока ты сделаешь шаг",
        "Стараюсь всё обсудить спокойно",
        "Мне нужно время остыть",
    ]),
    ("Что для меня важно в общении?", [
        "Чтобы меня слышали",
        "Чтобы не было давления",
        "Чтобы было интересно",
        "Чтобы было честно",
    ]),
    ("Как я обычно отмечаю важные события?", [
        "С близкими, дома",
        "В шумной компании",
        "Скромно, без большого размаха",
        "Как получится, без плана",
    ]),
    ("Что я скорее всего скажу, если мне не нравится идея?", [
        "Прямо скажу, что не нравится",
        "Промолчу, чтобы не обидеть",
        "Предложу альтернативу",
        "Соглашусь, но без энтузиазма",
    ]),
    ("Как я отношусь к тому, чтобы делиться личным?", [
        "Открыт(а) с близкими",
        "Дозирую информацию",
        "Предпочитаю держать при себе",
        "Зависит от человека",
    ]),
    ("Что мне помогает прийти в себя после тяжёлого дня?", [
        "Разговор с близким",
        "Тишина и одиночество",
        "Музыка или фильм",
        "Прогулка или спорт",
    ]),
    ("Как я понимаю, что человек мне действительно близок?", [
        "Когда могу быть собой",
        "Когда могу доверить тайну",
        "Когда могу попросить о помощи",
        "Когда просто хорошо молчим вместе",
    ]),
]

MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


# ============================================================
# ОБЩИЙ CSS
# ============================================================
BASE_STYLE = """
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #6d28d9 100%);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    overflow-x: hidden;
  }
  .card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 24px;
    padding: 36px 32px;
    max-width: 720px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    animation: fadeUp 0.7s ease both;
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  h1, h2 { margin-bottom: 16px; line-height: 1.25; }
  h1 { font-size: 2.1rem; }
  h2 { font-size: 1.5rem; }
  p  { line-height: 1.6; margin-bottom: 12px; color: #e0e7ff; }
  label { display: block; margin: 14px 0 6px; font-weight: 600; }
  input[type=text], input[type=number], select {
    width: 100%;
    padding: 12px 14px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.25);
    background: rgba(255,255,255,0.1);
    color: #fff;
    font-size: 1rem;
    outline: none;
    transition: border 0.2s, background 0.2s;
  }
  input[type=text]::placeholder,
  input[type=number]::placeholder { color: #c7d2fe; }
  input:focus, select:focus { border-color: #a78bfa; background: rgba(255,255,255,0.18); }
  option { color: #111; }
  .row { display: flex; gap: 14px; }
  .row > * { flex: 1; }
  button, .btn {
    display: inline-block;
    margin-top: 22px;
    padding: 14px 28px;
    font-size: 1.05rem;
    font-weight: 700;
    color: #1e1b4b;
    background: linear-gradient(135deg, #facc15, #fb923c);
    border: none;
    border-radius: 999px;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    box-shadow: 0 8px 24px rgba(250,204,21,0.35);
    text-decoration: none;
  }
  button:hover, .btn:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 12px 28px rgba(250,204,21,0.5);
  }

  /* Карточки «Кто ты мне?» — через JS, чтобы работало везде */
  .roles { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 8px; }
  .role {
    position: relative;
    padding: 16px;
    border-radius: 14px;
    border: 2px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.06);
    cursor: pointer;
    text-align: center;
    font-weight: 600;
    transition: all 0.2s;
    user-select: none;
  }
  .role input { position: absolute; opacity: 0; pointer-events: none; }
  .role:hover { border-color: #a78bfa; }
  .role.selected {
    border-color: #facc15;
    background: rgba(250,204,21,0.18);
    box-shadow: 0 0 20px rgba(250,204,21,0.4);
    transform: scale(1.03);
  }

  /* Прогресс-бар */
  .progress-wrap {
    width: 100%; height: 12px; border-radius: 999px;
    background: rgba(255,255,255,0.15); overflow: hidden;
    margin-bottom: 24px;
  }
  .progress-bar {
    height: 100%; width: 0%;
    background: linear-gradient(90deg, #34d399, #60a5fa, #a78bfa);
    transition: width 0.4s ease;
  }

  /* Варианты ответов */
  .option {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px; margin: 10px 0;
    border-radius: 14px;
    border: 2px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.06);
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
  }
  .option:hover { border-color: #a78bfa; background: rgba(167,139,250,0.15); }
  .option input { accent-color: #facc15; width: 20px; height: 20px; cursor: pointer; }
  .option.selected {
    border-color: #facc15;
    background: rgba(250,204,21,0.15);
    box-shadow: 0 0 16px rgba(250,204,21,0.35);
  }

  /* Красная тревожная плашка */
  .alert {
    background: #b91c1c;
    border: 3px solid #fecaca;
    border-radius: 20px;
    padding: 40px 28px;
    text-align: center;
    animation: pulse 0.8s infinite alternate, fadeUp 0.4s both;
    max-width: 720px;
    width: 100%;
  }
  @keyframes pulse {
    from { box-shadow: 0 0 30px rgba(239,68,68,0.6); transform: scale(1); }
    to   { box-shadow: 0 0 80px rgba(239,68,68,1);   transform: scale(1.02); }
  }
  .alert h1 { color: #fff; text-shadow: 0 0 12px #000; animation: blink 0.6s infinite alternate; }
  @keyframes blink { from { opacity: 1; } to { opacity: 0.45; } }

  .confetti-canvas { position: fixed; top:0; left:0; width:100%; height:100%; pointer-events: none; z-index: 9999; }
  .center { text-align: center; }
  .big { font-size: 3.5rem; font-weight: 800; color: #facc15; margin: 8px 0; }
  .muted { color: #c7d2fe; font-size: 0.95rem; }
</style>
"""


# ============================================================
# JS: конфетти (без внешних библиотек)
# ============================================================
CONFETTI_JS = """
<canvas class="confetti-canvas" id="confetti"></canvas>
<script>
(function(){
  var canvas = document.getElementById('confetti');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var W, H, parts = [];
  function resize(){ W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
  resize(); window.addEventListener('resize', resize);
  var colors = ['#facc15','#fb923c','#34d399','#60a5fa','#a78bfa','#f472b6','#ffffff'];
  function spawn(n){
    for (var i=0;i<n;i++){
      parts.push({
        x: Math.random()*W,
        y: -20 - Math.random()*H*0.3,
        vx: (Math.random()-0.5)*3,
        vy: 2 + Math.random()*4,
        s: 6 + Math.random()*8,
        c: colors[Math.floor(Math.random()*colors.length)],
        r: Math.random()*Math.PI,
        vr: (Math.random()-0.5)*0.2
      });
    }
  }
  spawn(180);
  function loop(){
    ctx.clearRect(0,0,W,H);
    for (var i = parts.length - 1; i >= 0; i--){
      var p = parts[i];
      p.x += p.vx; p.y += p.vy; p.r += p.vr; p.vy += 0.03;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.r);
      ctx.fillStyle = p.c;
      ctx.fillRect(-p.s/2, -p.s/2, p.s, p.s*0.6);
      ctx.restore();
      if (p.y > H + 30) parts.splice(i, 1);
    }
    // подсыпаем новые, чтобы конфетти не заканчивалось
    if (parts.length < 120 && Math.random() < 0.4) spawn(3);
    requestAnimationFrame(loop);
  }
  loop();
})();
</script>
"""


# ============================================================
# ЭКРАН 1 — ПРИВЕТСТВИЕ
# ============================================================
WELCOME = """
<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Привет!</title>""" + BASE_STYLE + """</head>
<body>
  <div class="card center">
    <h1>Привет, друг 👋</h1>
    <p>Я приготовил(а) для тебя маленький тест. Ничего серьёзного — просто проверю, насколько хорошо ты меня знаешь.</p>
    <p>Готов(а)? Тогда поехали 🚀</p>
    <a class="btn" href="/form">Начать</a>
  </div>
</body></html>
"""


# ============================================================
# ЭКРАН 2 — ФОРМА ЗНАКОМСТВА
# ============================================================
FORM = """
<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Давай познакомимся</title>""" + BASE_STYLE + """</head>
<body>
  <div class="card">
    <h2>Давай познакомимся 🙂</h2>
    <form method="POST" action="/quiz" id="form">
      <label for="name">Как тебя зовут?</label>
      <input type="text" id="name" name="name" placeholder="Например, Алексей" required>

      <label>Дата рождения</label>
      <div class="row">
        <select name="month" required>
          <option value="">Месяц</option>
          {% for m in months %}
            <option value="{{ loop.index0 }}">{{ m }}</option>
          {% endfor %}
        </select>
        <input type="number" name="day" min="1" max="31" placeholder="День" required>
      </div>

      <label>Кто ты мне?</label>
      <div class="roles" id="roles">
        <label class="role"><input type="radio" name="role" value="друг" required><span>🤝 Друг</span></label>
        <label class="role"><input type="radio" name="role" value="возлюбленный"><span>❤️ Возлюбленный</span></label>
        <label class="role"><input type="radio" name="role" value="фанат"><span>🤩 Фанат</span></label>
        <label class="role"><input type="radio" name="role" value="сталкер"><span>🕵️ Сталкер</span></label>
      </div>

      <button type="submit">Дальше →</button>
    </form>
  </div>
<script>
  // Подсветка выбранной карточки-роли (работает во всех браузерах)
  var roles = document.querySelectorAll('#roles .role');
  roles.forEach(function(label){
    label.addEventListener('click', function(){
      roles.forEach(function(l){ l.classList.remove('selected'); });
      label.classList.add('selected');
    });
  });
</script>
</body></html>
"""


# ============================================================
# ЭКРАН 3 — ОПРОС
# ============================================================
QUIZ = """
<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Опрос</title>""" + BASE_STYLE + """</head>
<body>
  <div class="card">
    <h2>Опрос: узнаю тебя поближе</h2>
    <div class="progress-wrap"><div class="progress-bar" id="bar"></div></div>

    <form method="POST" action="/result" id="quizForm">
      {% for q_text, q_options in questions %}
        {% set q_index = loop.index0 %}
        <div style="margin-bottom:22px;">
          <p style="font-weight:600;color:#fff;">{{ loop.index }}. {{ q_text }}</p>
          {% for opt in q_options %}
            <label class="option">
              <input type="radio" name="q{{ q_index }}" value="{{ opt }}" required>
              <span>{{ opt }}</span>
            </label>
          {% endfor %}
        </div>
      {% endfor %}
      <button type="submit">Завершить опрос ✅</button>
    </form>
  </div>
<script>
  // Прогресс-бар + подсветка выбранных вариантов
  var form = document.getElementById('quizForm');
  var bar  = document.getElementById('bar');
  var total = {{ questions|length }};

  form.addEventListener('change', function(){
    var names = new Set();
    form.querySelectorAll('input[type=radio]:checked').forEach(function(i){ names.add(i.name); });
    bar.style.width = (names.size / total * 100) + '%';

    form.querySelectorAll('.option').forEach(function(label){
      var inp = label.querySelector('input');
      if (inp && inp.checked) label.classList.add('selected');
      else label.classList.remove('selected');
    });
  });

  form.querySelectorAll('.option').forEach(function(label){
    label.addEventListener('click', function(){
      setTimeout(function(){
        var inp = label.querySelector('input');
        form.querySelectorAll('input[name="' + inp.name + '"]').forEach(function(other){
          other.closest('.option').classList.remove('selected');
        });
        if (inp.checked) label.classList.add('selected');
      }, 0);
    });
  });
</script>
</body></html>
"""


# ============================================================
# ЭКРАН 4 — РЕЗУЛЬТАТ
# ============================================================
RESULT = """
<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Результат</title>""" + BASE_STYLE + CONFETTI_JS + """</head>
<body>
  <div class="card center">
    <h2>{{ title }}</h2>
    <div class="big">{{ percent }}%</div>
    <p>Ты прошёл(ла) {{ percent }}% опроса!</p>
    <p>{{ message }}</p>
    <p class="muted">Секундочку… сейчас будет ещё кое-что 😏</p>
  </div>
<script>
  setTimeout(function(){ window.location.href = '/hacked'; }, 5000);
</script>
</body></html>
"""


# ============================================================
# ЭКРАН 5 — «ВАС ВЗЛОМАЛИ»
# ============================================================
HACKED = """
<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>!!!</title>""" + BASE_STYLE + """</head>
<body>
  <div class="alert">
    <h1>⚠️ ВНИМАНИЕ! ⚠️</h1>
    <h2>ВАШИ ДАННЫЕ БЫЛИ СКОМПРОМЕТИРОВАНЫ!</h2>
    <p style="color:#fee2e2;">Мы уже знаем: <b>{{ name }}</b>, {{ day }} {{ month }}, роль — {{ role }}.</p>
    <p style="color:#fee2e2;">Не выключайте компьютер. Идёт передача данных…</p>
  </div>
<script>
  setTimeout(function(){ window.location.href = '/final'; }, 10000);
</script>
</body></html>
"""


# ============================================================
# ЭКРАН 6 — ФИНАЛЬНАЯ ШУТКА
# ============================================================
FINAL = """
<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Шутка 😘</title>""" + BASE_STYLE + CONFETTI_JS + """</head>
<body>
  <div class="card center">
    <h1>Спасибо за данные, я пиздаболка 😘</h1>
    <p>Никакого взлома не было — просто шутка. Ты {{ name }}, и это было весело!</p>
    <p class="muted">Обнимаю. Ещё поиграем? 😄</p>
    <a class="btn" href="/">Ещё раз 🔁</a>
  </div>
</body></html>
"""


# ============================================================
# РОУТЫ
# ============================================================
@app.route("/")
def index():
    return render_template_string(WELCOME)


@app.route("/form")
def form():
    return render_template_string(FORM, months=MONTHS)


@app.route("/quiz", methods=["POST"])
def quiz():
    # Сохраняем данные формы в сессии
    session["name"] = request.form.get("name", "друг").strip() or "друг"
    month_idx = request.form.get("month", "0")
    try:
        session["month"] = MONTHS[int(month_idx)]
    except (ValueError, IndexError):
        session["month"] = "?"
    session["day"] = request.form.get("day", "?")
    session["role"] = request.form.get("role", "друг")
    return render_template_string(QUIZ, questions=QUESTIONS)


@app.route("/result", methods=["POST"])
def result():
    # Считаем ответы: вопросов ровно len(QUESTIONS), имена полей q0..qN-1
    answers = []
    for i in range(len(QUESTIONS)):
        val = request.form.get("q{}".format(i))
        if val:
            answers.append(val)

    total = len(QUESTIONS)
    answered = len(answers)
    percent = int(round(answered / total * 100)) if total else 0

    # Логика: 100% ответов = поздравление, иначе — шутливый «проигрыш».
    # Хочешь рандом — замени условие на random.choice([True, False]).
    if answered == total:
        title = "🎉 Поздравляем!"
        message = "Ты ответил(а) на все вопросы! Ты официально знаешь меня лучше всех."
    else:
        title = "😅 Почти получилось!"
        message = "Ты ответил(а) не на все вопросы, но это тоже результат!"

    return render_template_string(
        RESULT,
        title=title,
        message=message,
        percent=percent,
    )


@app.route("/hacked")
def hacked():
    return render_template_string(
        HACKED,
        name=session.get("name", "друг"),
        day=session.get("day", "?"),
        month=session.get("month", "?"),
        role=session.get("role", "друг"),
    )


@app.route("/final")
def final():
    return render_template_string(FINAL, name=session.get("name", "друг"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)