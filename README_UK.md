# ====================================================================================================
# 🧠⚙️ PHYSICS-INFORMED ІНТЕЛЕКТУАЛЬНА СИСТЕМА КОНТРОЛЮ ЯКОСТІ ОБЛІКУ ПРИРОДНОГО ГАЗУ
# ====================================================================================================

## 📌 Загальний опис

Даний програмний комплекс реалізує повний цикл **physics-informed аналізу якості обліку природного газу** з використанням:
- методів машинного навчання;
- фізичних моделей транспортування газу;
- реконструкції часових рядів;
- інтелектуального аналізу аномалій;
- метролого-орієнтованого контролю достовірності.

Система поєднує:
✅ реальні дані газових вузлів обліку;  
✅ physics-informed моделювання;  
✅ алгоритми anomaly detection;  
✅ реконструкцію високочастотних сигналів;  
✅ генерацію фізично правдоподібних аномалій;  
✅ автоматичне benchmark-порівняння моделей.

---

# 🎯 Основне призначення комплексу

Програмний комплекс призначений для створення експериментального середовища дослідження:

- достовірності обліку природного газу;
- деградації сенсорів;
- локальних витоків;
- метрологічних порушень;
- аномальної поведінки вузлів обліку;
- інтелектуального контролю енергоносіїв.

---

# 🧪 Основні задачі системи

Система реалізує одночасно декілька наукових та прикладних задач:

## 📥 Завантаження реальних даних

Підтримується обробка:
- реальних часових рядів;
- телеметрії витратомірів;
- даних SCADA;
- експериментальних вимірювань.

---

## 🔄 Реконструкція часових рядів

Реальні промислові дані часто мають:
- низьку часову роздільність;
- втрати даних;
- пропуски;
- асинхронність.

Система виконує:
✅ реконструкцію 1-секундного сигналу;  
✅ інтерполяцію часових рядів;  
✅ physics-aware згладжування;  
✅ PID-inspired реконструкцію.

---

## ⚠️ Генерація фізично правдоподібних аномалій

Програмний комплекс дозволяє:
- ін’єктувати аномалії;
- моделювати деградацію;
- відтворювати аварійні режими.

---

# 🔬 Наукова мотивація

У сфері комерційного обліку природного газу практично відсутні відкриті datasets через:

🔒 комерційну таємницю;  
🔒 критичність інфраструктури;  
🔒 кібербезпекові ризики;  
🔒 обмежений доступ до SCADA-систем.

Тому класичні ML-підходи часто тестуються лише на synthetic data, що:
- знижує достовірність;
- спрощує задачу;
- не враховує фізику процесу.

---

# 💡 Запропонований підхід

Для подолання цих обмежень реалізовано:

# 🌐 HYBRID PHYSICS-INFORMED BENCHMARK

який поєднує:

✅ реальні сигнали витратомірів;  
✅ фізичні моделі транспортування газу;  
✅ контрольовану генерацію аномалій;  
✅ physics-aware реконструкцію;  
✅ інтелектуальну аналітику.

---

# 🏗 Архітектура програмного комплексу

# 1️⃣ Завантаження реальних даних

Система працює з файлами типу:

```csv
time,black,gray
15,2084,2095
17.5,2086,2097
20,2089,2099
де:

time — часові відмітки;
black — основний сигнал витратоміра;
gray — допоміжний канал.
2️⃣ Реконструкція сигналу

Реальні дані мають дискретність:

Δt = 15 секунд

Для ML-аналізу цього недостатньо.

Тому система виконує:

cubic spline interpolation;
PID-inspired reconstruction;
фізично обмежене згладжування.
🧠 Physics-informed reconstruction

Реконструкція враховує:

✅ інерційність газового потоку;
✅ обмеження швидкості зміни витрати;
✅ фізичну плавність сигналу;
✅ динаміку трубопроводу.

📐 Cubic Spline

Для кожного інтервалу будується кубічний поліном:

S
i
	​

(x)=a
i
	​

+b
i
	​

(x−x
i
	​

)+c
i
	​

(x−x
i
	​

)
2
+d
i
	​

(x−x
i
	​

)
3

що забезпечує:

безперервність;
гладкість;
фізично реалістичний сигнал.
⚙️ PID-inspired reconstruction

На відміну від класичного PID-регулятора,
запропонований алгоритм працює у:

🔁 зворотному напрямку

тобто:

не керує процесом;
а реконструює відсутні значення.
📐 Помилка реконструкції
e(t)=x
target
	​

(t)−x
current
	​

(t)
📐 Оновлення сигналу
u(t)=K
p
	​

e(t)+K
d
	​

dt
de(t)
	​

🚫 Фізичні обмеження

Система запобігає:

нереалістичним стрибкам;
надмірним осциляціям;
високочастотному шуму.
⚠️ Ін’єкція аномалій включає

🔬 Sensor Drift Injection

Моделюється:

старіння сенсора;
температурний drift;
деградація АЦП;
метрологічний дрейф.
🌫 Leakage Injection

Моделюються:

локальні витоки;
розгерметизація;
втрати газу;
несанкціонований відбір.

📡 Noise Burst Injection

Імітуються:

електромагнітні завади;
короткочасний шум;
нестабільність сигналу;
порушення телеметрії.

⏱ Desynchronization Injection

Моделюється:

часовий зсув;
несинхронність SCADA;
затримки вузлів збору даних.


🤖 Алгоритми машинного навчання

Програмний комплекс підтримує benchmark-порівняння:

Метод	Опис
Isolation Forest	Ізоляція аномалій деревами
DBSCAN	Кластеризація та пошук outliers
Autoencoder	Нейромережевий reconstruction-based підхід
Kalman Filter	Статистичне фільтрування
Double Control	Physics-informed hybrid метод
🧠 Double Control Method

Центральним елементом системи є:

⚡ МЕТОД ПОДВІЙНОГО КОНТРОЛЮ
🔹 Рівень 1 — Statistical Control

Аналіз:

часових рядів;
reconstruction error;
ML-відхилень.
🔹 Рівень 2 — Physical Control

Перевірка:

балансової узгодженості;
фізичної правдоподібності;
динаміки потоку;
інваріантів системи.
📊 Метрики оцінювання

Автоматично обчислюються:

✅ ROC-AUC
✅ Precision
✅ Recall
✅ F1-score

📈 Візуалізація

Система автоматично генерує:

🖼 ROC-криві
🖼 графіки сигналів
🖼 anomaly injection plots
🖼 benchmark diagrams
🖼 comparative figures

🗂 Структура результатів
data/
├── plots/
│   ├── roc_curves.png
│   ├── anomaly_signal.png
│
├── results/
│   ├── model_comparison.csv
│   ├── benchmark_dataset.csv
📦 Benchmark Dataset

Сформований dataset містить:

✅ нормальні сигнали;
✅ сигнали з аномаліями;
✅ labels;
✅ anomaly scores;
✅ predictions моделей.

🧪 Призначення benchmark dataset

Dataset може використовуватись для:

навчання ML;
benchmark testing;
reproducible research;
порівняння алгоритмів;
оцінки physics-informed AI.
🚀 Переваги запропонованого підходу

У порівнянні з purely synthetic datasets:

Classical Synthetic	Proposed Physics-Informed
Низька реалістичність	Реальні сигнали
Випадкові аномалії	Фізично правдоподібні
Відсутність фізики	Physics-aware
Спрощені моделі	Реальні режими
Погана інтерпретація	Explainable AI
🌐 Потенційні області застосування

Система може використовуватись у:

✅ Smart Gas Infrastructure
✅ SCADA Diagnostics
✅ Industrial AI
✅ Digital Twins
✅ Predictive Maintenance
✅ Cyber-Physical Systems
✅ Intelligent Metering
✅ Energy Monitoring
✅ Industrial Anomaly Detection

📚 Наукова новизна

Програмний комплекс реалізує:

✅ hybrid physics-informed benchmark;
✅ reconstruction-aware anomaly detection;
✅ physics-aware telemetry analysis;
✅ інтелектуальний контроль якості обліку;
✅ поєднання ML та фізичних моделей.

🧩 Cтруктура проєкту 
```
.
├── requirements.txt
├── README.md
├── data/
│   ├── raw/                # оригінальні CSV
│   ├── processed/          # проміжні результати
│   ├── plots/              # графіки
│   └── results/            # таблиці, dataset, порівняння
├── scripts/
│   └── run_pipeline.py
└── src/
	└── gas_quality/
		├── __init__.py
		├── cli.py
		├── pipeline.py
		├── config.py
		├── io.py
		├── preprocessing.py
		├── reconstruction.py
		├── evaluation.py
		├── visualization.py
		├── anomalies/
		│   ├── __init__.py
		│   ├── injection.py
		│   └── detectors.py
		└── double_control/
			├── __init__.py
			├── statistical.py
			└── physical.py
```
⚙️ Вимоги

Рекомендоване середовище:

Python 3.11+
NumPy
Pandas
SciPy
Matplotlib
Scikit-learn
📥 Встановлення
pip install numpy pandas scipy matplotlib scikit-learn
▶️ Запуск
python main.py
🔮 Подальший розвиток

Планується інтеграція:

✅ LSTM
✅ Transformer architectures
✅ Graph Neural Networks
✅ Digital Twins
✅ Online Monitoring
✅ Adaptive Thresholding
✅ Multi-Agent Systems
✅ Retrieval-Augmented Diagnostics

👨‍🔬 Авторська концепція

Проєкт орієнтований на дослідження:

інтелектуального обліку енергоносіїв;
physics-informed AI;
anomaly detection;
industrial machine learning;
кіберфізичних систем;
explainable AI;
метрологічної достовірності.
====================================================================================================
⚡ PHYSICS-INFORMED AI FOR SMART GAS METERING ⚡
====================================================================================================

---

# 🖥️ Користувацький Інтерфейс (SCADA-подібна система)

## 🎮 Запуск GUI Оператора

Система включає інтерактивне вікно оператора для моніторингу Double Control в реальному часі:

```bash
python scripts/run_gui.py
# або
python -m src.gas_quality.cli --gui
```

### Можливості GUI:
- 📊 Завантаження метрологічних даних з CSV
- 🔄 Реконструкція сигналів у реальному часі
- ⚙️ Запуск методу подвійного контролю
- 📈 Візуалізація сигналів і anomaly scores
- 🚨 Індикатори вердикту (NORMAL / ANOMALY DETECTED)
- 📋 Таблиця результатів (Level 1, Level 2, Final Decision)
- 💾 Експорт звіту в текстовий файл

---

# 🔬 Метод Подвійного Контролю (Реалізація)

## 📋 Структура Контролю

### Рівень 1: Статистичний Контроль (L1)
Перевіряє:
- Помилка реконструкції сигналу
- Z-score відхилення (rolling statistics)
- Isolation Forest anomaly detection
- **Вихід:** комбінований score (0..1)

### Рівень 2: Фізичний Контроль (L2)
Перевіряє:
- Балансова невв'язка (Qin - (Qout + Qcons + Qacc))
- Градієнт потоку (максимальна швидкість зміни)
- Кореляція тиску та потоку
- Зміни температури
- **Вихід:** комбінований score (0..1)

### Фінальне Рішення
- **Режим "weighted"** (за замовчуванням): комбінація L1 + L2
- **Режим "strict"**: обидва рівні мають узгодитися (AND)
- **Вердикт:** NORMAL або ANOMALY DETECTED

---

# 🚀 Швидкий Старт

## 1. Встановлення залежностей
```bash
pip install -r requirements.txt
```

## 2. Генерація тестових даних
```bash
python scripts/generate_test_data.py
```

## 3. Запуск CLI pipeline
```bash
python -m src.gas_quality.cli --cli
```

## 4. Запуск GUI оператора
```bash
python scripts/run_gui.py
```

## 5. Запуск через notebook
```bash
jupyter notebook notebooks/pipeline_example.ipynb
```

---

# 📦 Вимоги

```
Python 3.11+
NumPy
Pandas
SciPy
Matplotlib
Scikit-learn
pytest
```

---

# 🧬 Архітектура Модулів

| Модуль | Призначення |
|--------|-----------|
| `config.py` | Конфігурація шляхів і константи |
| `io.py` | Завантаження/збереження даних |
| `preprocessing.py` | Очищення та підготовка |
| `reconstruction.py` | Cubic Spline + PID-inspired |
| `anomalies/injection.py` | Генерація фізичних аномалій |
| `anomalies/detectors.py` | ML-детектори (IF, DBSCAN, AE) |
| `double_control/statistical.py` | Level 1: Статистичний контроль |
| `double_control/physical.py` | Level 2: Фізичний контроль |
| `double_control/__init__.py` | Оркестратор подвійного контролю |
| `evaluation.py` | Метрики (ROC-AUC, Precision, F1) |
| `visualization.py` | Графіки ROC та сигналів |
| `benchmark.py` | Pipeline для benchmark |
| `gui.py` | SCADA-подібна система |
| `pipeline.py` | Головний оркестратор (CLI/GUI) |
| `cli.py` | Інтерфейс командного рядка |

---

# 📊 Вихідні Дані

Система генерує та зберігає:

```
data/
├── raw/
│   ├── rec_date.csv              # Вхідні дані з витратоміра (15 сек)
│   └── metrological_data.csv     # Метрологічні дані
├── processed/
│   └── [проміжні файли]
├── plots/
│   ├── roc_curves.png
│   ├── anomaly_signal.png
│   └── reconstruction_preview.png
└── results/
    ├── benchmark_dataset.csv     # Вихідний dataset
    └── model_comparison.csv      # Порівняння моделей
```

---

# 🔄 Робочий процес

```
1. Завантажити rec_date.csv
   ↓
2. Реконструювати 1-секундний сигнал (Cubic Spline + PID)
   ↓
3. Ін'єктувати контрольовані аномалії (drift, leak, spike)
   ↓
4. Запустити L1 (Statistical Control)
   ↓
5. Запустити L2 (Physical Control)
   ↓
6. Фінальне рішення (комбіновані scores)
   ↓
7. Експортувати звіт та графіки
```

---

# 🧪 Тестування

```bash
pytest -v
pytest tests/test_reconstruction.py
pytest tests/test_injection.py
pytest tests/test_physical_control.py
```

---

# 👨‍💻 Розробка

Для розширення системи:

1. **Додати новий детектор:** `src/gas_quality/anomalies/detectors.py`
2. **Модифікувати L1/L2:** редагувати `src/gas_quality/double_control/*.py`
3. **Розширити GUI:** дополнити `src/gas_quality/gui.py`
4. **Додати тести:** писати в `tests/`

---

# 📝 Ліцензія

MIT License

---

# 👥 Автори

Physics-Informed AI Research Team

---