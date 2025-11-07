/* ===========================================================
   STARFIELD + AURORA BACKGROUND SCRIPT
   Author: Sowmya Sivan (with ChatGPT assistance)
   Description: Creates a parallax starfield background with
   gradient motion, random welcome message, and gentle chime.
   =========================================================== */

// ======= CONFIGURATION ======= //
const config = {
  starColor: ["#ffffff", "#cfe2ff", "#e6d9ff"], // star colors
  minStarSize: 0.8, // in px
  maxStarSize: 2.0,
  maxStarsDesktop: 200,
  maxStarsTablet: 150,
  maxStarsMobile: 110,
  parallaxIntensity: 0.15, // mouse speed sensitivity
  fadeInDuration: 2000, // background fade-in (ms)
  welcomeDuration: 2000, // how long the welcome message stays (ms)
  chimeVolume: 0.2 // gentle volume for the welcome chime
};

// ======= DOM ELEMENTS ======= //
const canvas = document.getElementById("starfield");
const ctx = canvas.getContext("2d");
const toggleBtn = document.getElementById("toggleStars");
const welcomeEl = document.getElementById("welcomeMessage");

// ======= STATE VARIABLES ======= //
let stars = [];
let animationActive = true;
let mouse = { x: 0, y: 0 };
let lastMouseMove = Date.now();
let welcomeShown = false;

// ======= DETERMINE DEVICE TYPE ======= //
function getStarCount() {
  if (window.innerWidth > 1024) return config.maxStarsDesktop;
  if (window.innerWidth > 600) return config.maxStarsTablet;
  return config.maxStarsMobile;
}

// ======= INITIALIZE CANVAS ======= //
function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// ======= STAR OBJECT ======= //
class Star {
  constructor() {
    this.reset();
  }
  reset() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.size =
      config.minStarSize +
      Math.random() * (config.maxStarSize - config.minStarSize);
    this.speed = 0.05 + Math.random() * 0.1;
    this.color =
      config.starColor[Math.floor(Math.random() * config.starColor.length)];
    this.alpha = 0.5 + Math.random() * 0.5;
    this.parallaxDepth = Math.random() * 2; // for depth effect
  }
  update() {
    this.y -= this.speed;
    if (this.y < -this.size) {
      this.y = canvas.height + this.size;
      this.x = Math.random() * canvas.width;
    }
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${hexToRgb(this.color)},${this.alpha})`;
    ctx.shadowBlur = 1.2;
    ctx.shadowColor = this.color;
    ctx.fill();
  }
}

// ======= UTILITY: HEX TO RGB ======= //
function hexToRgb(hex) {
  const shorthand = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
  hex = hex.replace(shorthand, (m, r, g, b) => r + r + g + g + b + b);
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? `${parseInt(result[1], 16)},${parseInt(result[2], 16)},${parseInt(
        result[3],
        16
      )}`
    : null;
}

// ======= CREATE STARS ======= //
function createStars() {
  stars = [];
  const count = getStarCount();
  for (let i = 0; i < count; i++) {
    stars.push(new Star());
  }
}

// ======= DRAW LOOP ======= //
function animate() {
  if (!animationActive) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Calculate parallax shift from mouse velocity
  const delta = (Date.now() - lastMouseMove) / 1000;
  const offsetX = (mouse.x - canvas.width / 2) * config.parallaxIntensity;
  const offsetY = (mouse.y - canvas.height / 2) * config.parallaxIntensity;

  for (let s of stars) {
    s.update();
    ctx.save();
    ctx.translate(-offsetX / s.parallaxDepth, -offsetY / s.parallaxDepth);
    s.draw();
    ctx.restore();
  }

  requestAnimationFrame(animate);
}

// ======= MOUSE MOVEMENT (PARALLAX CONTROL) ======= //
window.addEventListener("mousemove", (e) => {
  const speedX = Math.abs(e.movementX);
  const speedY = Math.abs(e.movementY);
  const intensity = Math.min(1, (speedX + speedY) / 50);
  config.parallaxIntensity = 0.1 + intensity * 0.25;
  mouse.x = e.clientX;
  mouse.y = e.clientY;
  lastMouseMove = Date.now();
});

// ======= TOUCH SUPPORT ======= //
window.addEventListener("touchmove", (e) => {
  const touch = e.touches[0];
  mouse.x = touch.clientX;
  mouse.y = touch.clientY;
});

// ======= TOGGLE ANIMATION ======= //
toggleBtn.addEventListener("click", () => {
  animationActive = !animationActive;
  toggleBtn.textContent = animationActive ? "🌙" : "☀️";
  if (animationActive) {
    animate();
  }
});

// ======= WELCOME MESSAGE LOGIC ======= //
const welcomeMessages = [
  "Welcome to my galaxy ✨",
  "Hey buddy, ready to explore? 🚀",
  "Shining bright, aren’t we? 🌟",
  "Let’s start an amazing journey 💫",
  "Hi there, explorer of code! 💻💜"
];

function showWelcomeMessage() {
  if (welcomeShown) return;
  welcomeShown = true;

  // Pick random phrase
  const randomMsg =
    welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
  welcomeEl.textContent = randomMsg;

  // Fade in
  welcomeEl.classList.add("show");
  playChime();

  // Fade out after delay
  setTimeout(() => {
    welcomeEl.classList.remove("show");
    welcomeEl.classList.add("fade");
  }, config.welcomeDuration);
}

// ======= CHIME SOUND (EMBEDDED BASE64) ======= //
function playChime() {
  try {
    const audio = new Audio(
      "data:audio/mp3;base64,//uQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAACcQCA..."
    );
    audio.volume = config.chimeVolume;
    audio.play().catch(() => {});
  } catch (err) {
    console.warn("Chime playback failed:", err);
  }
}

// ======= INITIALIZE EVERYTHING ======= //
window.addEventListener("load", () => {
  createStars();

  // Fade in background
  setTimeout(() => {
    canvas.style.opacity = "1";
  }, 100);

  // Start star animation
  animate();

  // Show welcome message
  showWelcomeMessage();
});
