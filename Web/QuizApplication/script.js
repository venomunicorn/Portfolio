const questions = [
    {
        question: "Which language runs in a web browser?",
        options: ["Java", "C", "Python", "JavaScript"],
        correct: 3
    },
    {
        question: "What does CSS stand for?",
        options: ["Central Style Sheets", "Cascading Style Sheets", "Cascading Simple Sheets", "Cars SUVs Sailboats"],
        correct: 1
    },
    {
        question: "What does HTML stand for?",
        options: ["Hypertext Markup Language", "Hypertext Markdown Language", "Hyperloop Machine Language", "Helicopters Terminals Motorboats Lamborginis"],
        correct: 0
    },
    {
        question: "Which year was JavaScript launched?",
        options: ["1996", "1995", "1994", "None of the above"],
        correct: 1
    },
    {
        question: "Who developed Python?",
        options: ["Brendan Eich", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup"],
        correct: 1
    }
];

let currentQuestion = 0;
let score = 0;

const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options');
const progressFill = document.getElementById('progress');
const questionCount = document.getElementById('question-count');
const scoreDisplay = document.getElementById('score');
const quizCard = document.getElementById('quiz-card');
const resultCard = document.getElementById('result-card');
const finalScore = document.getElementById('final-score');
const feedbackText = document.getElementById('feedback-text');

function loadQuestion() {
    const q = questions[currentQuestion];
    questionText.textContent = q.question;
    optionsContainer.innerHTML = '';

    q.options.forEach((opt, index) => {
        const btn = document.createElement('button');
        btn.textContent = opt;
        btn.classList.add('btn-option');
        btn.onclick = () => selectOption(index, btn);
        optionsContainer.appendChild(btn);
    });

    // Update Header
    questionCount.textContent = `Question ${currentQuestion + 1}/${questions.length}`;
    progressFill.style.width = `${((currentQuestion) / questions.length) * 100}%`;
}

function selectOption(index, btn) {
    // Disable all buttons
    const buttons = optionsContainer.querySelectorAll('.btn-option');
    buttons.forEach(b => b.disabled = true);

    const correctIndex = questions[currentQuestion].correct;

    if (index === correctIndex) {
        btn.classList.add('correct');
        score++;
        scoreDisplay.textContent = `Score: ${score}`;
    } else {
        btn.classList.add('wrong');
        buttons[correctIndex].classList.add('correct'); // Show correct answer
    }

    setTimeout(() => {
        currentQuestion++;
        if (currentQuestion < questions.length) {
            loadQuestion();
        } else {
            showResult();
        }
    }, 1500);
}

function showResult() {
    quizCard.classList.add('hidden');
    resultCard.classList.remove('hidden');
    finalScore.textContent = score;
    progressFill.style.width = '100%';

    if (score === questions.length) {
        feedbackText.textContent = "Perfect Score! 🏆";
    } else if (score > questions.length / 2) {
        feedbackText.textContent = "Great Job! Keep it up! 👍";
    } else {
        feedbackText.textContent = "Keep practicing! 💪";
    }
}

// Start
loadQuestion();
