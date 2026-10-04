const frames = [
  'assets/nightmare-rain-01.png',
  'assets/nightmare-rain-02.png',
  'assets/nightmare-rain-03.png',
  'assets/nightmare-rain-04.png'
];
const stage = document.querySelector('.stage');
const a = document.getElementById('rainA');
const b = document.getElementById('rainB');
const toggle = document.getElementById('toggle');
const intensity = document.getElementById('intensity');
const speed = document.getElementById('speed');
let index = 0;
let active = true;
let timer;
let front = a;
let back = b;
function applyIntensity(){
  const v = Number(intensity.value) / 100;
  front.style.opacity = active ? v : 0;
}
function tick(){
  index = (index + 1) % frames.length;
  back.src = frames[index];
  const v = Number(intensity.value) / 100;
  back.style.opacity = active ? v : 0;
  front.style.opacity = 0;
  [front, back] = [back, front];
  clearTimeout(timer);
  timer = setTimeout(tick, Number(speed.value));
}
function restart(){ clearTimeout(timer); timer = setTimeout(tick, Number(speed.value)); }
toggle.addEventListener('click', () => {
  active = !active;
  stage.classList.toggle('off', !active);
  toggle.textContent = active ? 'Deactivate Nightmare Frequency' : 'Activate Nightmare Frequency';
  if (active) applyIntensity();
});
intensity.addEventListener('input', applyIntensity);
speed.addEventListener('input', restart);
applyIntensity();
restart();
