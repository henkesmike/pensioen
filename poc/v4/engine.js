const element = id => document.getElementById(id);
const audio = element('audio');
const caption = element('caption');
const path = element('flowpath');
const pathLength = path.getTotalLength();
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

function animateActor({ id, x, phase, period }, time) {
    const breath = 1 + animation.ademhalen.amplitude *
        Math.sin(time * 2 * Math.PI / animation.ademhalen.cyclus_seconden + phase);
    const sway = animation.zwaaien.amplitude *
        Math.sin(time * 2 * Math.PI / animation.zwaaien.cyclus_seconden + phase);
    element('motion-' + id).setAttribute(
        'transform',
        `translate(${x} 342) rotate(${sway}) scale(${1 + (breath - 1) * animation.ademhalen.verticale_factor} ${breath}) translate(${-x} -342)`
    );
    const cycle = (time + phase + animation.knipperen.fase_offset_seconden) % period;
    const duration = animation.knipperen.duur_seconden;
    const blink = cycle < duration && Math.sin(Math.PI * cycle / duration) > animation.knipperen.drempel;
    opacity('blink-' + id, Number(blink));
}

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

function draw() {
    const time = audio.currentTime;
    const cue = timeline.findLast(({ start }) => start <= time) ?? timeline[0];
    if (caption.textContent !== cue.text) caption.textContent = cue.text;

    const frame = Object.fromEntries(Array.from(tracks, ([id, track]) => [
        id,
        valueAt(track.findLast(({ start }) => start <= time) ?? track[0], time),
    ]));
    for (const [id, value] of Object.entries(frame)) {
        if (id !== 'income' && id !== 'bar') opacity(id, value);
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
    requestAnimationFrame(draw);
}

draw();
