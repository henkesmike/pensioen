const element = id => document.getElementById(id);
const audio = element('audio');
const caption = element('caption');
const path = element('flowpath');
let pathLength = 0;
const clamp = value => Math.max(0, Math.min(1, value));
const opacity = (id, value) => element(id).setAttribute('opacity', value);

const coins = Array.from({ length: 7 }, () => {
    const coin = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    coin.setAttribute('r', 9);
    coin.setAttribute('fill', '#d6aa55');
    coin.setAttribute('stroke', '#b7893d');
    element('coins').append(coin);
    return coin;
});

const actors = runtimeConfig.personages;
const animation = runtimeConfig.animaties;

const blinkStarts = [1.2, 3.28, 5.2, 5.68];
const blinkDurations = [.159, .106, .106, .106].map(duration => duration * 2.7);

function chooseCharacters(tone, combination) {
    const [person, partner] = combination;
    const tones = 'ABC';
    const partnerTone = person === partner ? tones[(tones.indexOf(tone) + 1) % tones.length] : tone;
    return [person + tone, partner + partnerTone];
}

function setActor({id, x}, sprite) {
    const img = element('sprite-' + id);
    const left = x - sprite.width / 2;
    img.setAttribute('x', left);
    img.setAttribute('width', sprite.width);
    img.setAttribute('href', sprite.image);
    element('blink-' + id).innerHTML = sprite.eyes.map(([x, y, rx, ry]) => {
        const cx = left + x;
        const cy = 62 + y;
        const line = rx * .76;
        return `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${sprite.tone}"/>
                <path d="M${cx-line} ${cy} q${line} ${ry*.42} ${line*2} 0" fill="none" stroke="#51372a" stroke-width=".8"/>`;
    }).join('');
    if (id === 'neutral') {
        const { image, left: mouthLeft, top, width, height } = sprite.mouth;
        const x = left + mouthLeft;
        const y = 62 + top;
        for (const [key, value] of Object.entries({href:image,x,y,width,height})) {
            element('mond-neutraal').setAttribute(key,value);
        }
        for (const [key, value] of Object.entries({cx:x+width/2,cy:y+height/2,rx:width/2,ry:height/2})) {
            element('mond-ellips').setAttribute(key,value);
        }
    }
}

function selectSituation(tone, combination) {
    const [person, partner] = chooseCharacters(tone, combination);
    for (const actor of actors) {
        const figure = actor.id === 'man' ? person : partner;
        setActor(actor, runtimeConfig.figuren[figure]);
    }
}

function animateActor({ id, x, phase, period }, time) {
    const amount = (1 - Math.cos((time + phase) * 2 * Math.PI / animation.ademhalen.cyclus_seconden)) / 2;
    element('motion-' + id).setAttribute('transform',
        `translate(${x} 342) scale(${1 + .009 * .7 * amount} ${1 + .014 * .7 * amount}) translate(${-x} -342)`);
    const cycle = (time + phase) % period;
    const blink = blinkStarts.some((start, i) => cycle >= start && cycle < start + blinkDurations[i]);
    opacity('blink-' + id, Number(blink));
}

element('situation').addEventListener('submit', event => {
    event.preventDefault();
    const selection = element('selection');
    const film = element('film');
    const error = element('preview-error');
    error.hidden = true;
    film.hidden = false;
    try {
        pathLength = path.getTotalLength();
        selectSituation(element('tone').value, element('couple').value);
        selectPlan(element('plan').value);
        draw();
        selection.hidden = true;
        element('edit-situation').focus();
    } catch (problem) {
        film.hidden = true;
        selection.hidden = false;
        error.hidden = false;
        console.error(problem);
    }
});

element('edit-situation').addEventListener('click', () => {
    audio.pause();
    cancelAnimationFrame(nextFrame);
    element('film').hidden = true;
    element('selection').hidden = false;
    element('tone').focus();
});

function valueAt({ start, from, to, duration }, time) {
    return duration ? from + (to - from) * clamp((time - start) / duration) : to;
}

const tracks = new Map();
for (const { start, changes } of timeline) {
    for (const [id, { to, duration }] of Object.entries(changes)) {
        if (!tracks.has(id)) tracks.set(id, []);
        const track = tracks.get(id);
        const from = track.length ? valueAt(track.at(-1), start) : to;
        track.push({ start, from, to, duration });
    }
}

let nextFrame = 0;
function draw() {
    if (element('film').hidden) return;
    const time = audio.currentTime;
    const cue = timeline.findLast(({ start }) => start <= time) ?? timeline[0];
    if (caption.textContent !== cue.text) caption.textContent = cue.text;

    const frame = Object.fromEntries(Array.from(tracks, ([id, track]) => [
        id,
        valueAt(track.findLast(({ start }) => start <= time) ?? track[0], time),
    ]));
    for (const [id, value] of Object.entries(frame)) {
        if (id !== 'income' && id !== 'bar' && id !== 'happy') opacity(id, value);
    }
    element('bar').setAttribute('width', 247 * frame.bar);

    opacity('flowpath', frame.income ? 0.65 : 0);
    coins.forEach((coin, index) => {
        const progress = (time * 0.52 + index / coins.length) % 1;
        const point = path.getPointAtLength(progress * pathLength);
        coin.setAttribute('cx', point.x);
        coin.setAttribute('cy', point.y);
        coin.setAttribute('opacity', Number(index < Math.round(coins.length * frame.income)));
    });
    actors.forEach(actor => animateActor(actor, time));
    nextFrame = requestAnimationFrame(draw);
}

draw();
