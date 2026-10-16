"""Plot the combined comparison, explicitly marking October 16 additions."""
from hashlib import sha256
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from plot_matched import SHORT as ORIGINAL_SHORT

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'overall_2026-10-16'
DEST = ROOT / 'figures'
SHORT = {**ORIGINAL_SHORT, 'microsoft_decision': 'Microsoft-Decision-1',
         'nimble_v4': 'Nimble v4', 'nimble_v4_max': 'Nimble v4 Max'}


def save(fig, name):
    for extension in ('png', 'svg'):
        target = DEST / ('overall_' + name + '.' + extension)
        fig.savefig(target, dpi=170,
                    bbox_inches='tight', facecolor='white')
        if extension == 'svg':
            target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines()) + '\n')
    plt.close(fig)


def main():
    summary = json.loads((SOURCE / 'summary.json').read_text())
    models = summary['models']
    added = set(summary['added_model_ids'])
    native = {'jev113', 'jev114', 'luna_decisions'} | added
    names = {m: SHORT[m] + (' *' if m in added else '') for m in models}
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.titleweight': 'bold'})
    order = sorted(models, key=lambda m: models[m]['primary']['correct'])
    height = max(8, len(order) * .55 + 2)
    fig, ax = plt.subplots(figsize=(13, height))
    y = np.arange(len(order))
    full = [100 * models[m]['primary']['accuracy_attempted'] for m in order]
    core = [100 * models[m]['by_role']['core']['accuracy_attempted'] for m in order]
    bars = ax.barh(y - .1, full, height=.48,
                   color=['#163e65' if m in native else '#18867d' for m in order])
    for m, bar in zip(order, bars):
        if m in added:
            bar.set_hatch('//')
            bar.set_edgecolor('#7599ba')
    ax.scatter(core, y + .22, marker='D', s=30, color='#efb83d',
               edgecolors='#6b511a', zorder=3, label='640 core questions')
    for i, model in enumerate(order):
        ax.text(full[i] + 1, i - .1, f"{full[i]:.1f}% ({models[model]['primary']['correct']}/1,136)", va='center')
    ax.set_yticks(y, [names[m] for m in order])
    ax.set_xlim(0, 111)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel('Correct / all 1,136 planned questions (%)')
    ax.set_title(f'{len(models)} models on the same text decision bank', loc='left', fontsize=18, pad=30)
    ax.text(0, 1.025, 'Navy: native Decisions. Teal: regular LLMs, switchable reasoning off. * Added October 16.', transform=ax.transAxes)
    ax.legend(frameon=False, loc='lower right')
    ax.grid(axis='x', alpha=.17)
    ax.set_axisbelow(True)
    fig.text(.18, .025, 'Original eleven: October 15, 2026. Hatched additions: October 16 (Toronto). First attempts only; failures unsuccessful.\nSame frozen questions and options. Related variants are not independent observations.', fontsize=9, color='#45535c')
    fig.subplots_adjust(left=.24, bottom=.13, top=.9)
    save(fig, 'accuracy')

    columns = sorted(models, key=lambda m: -models[m]['primary']['correct'])
    data = np.array([[100 * f['models'][m]['accuracy_attempted'] for m in columns] for f in summary['by_family']])
    fig, ax = plt.subplots(figsize=(max(17, len(columns) * .9 + 5), 14))
    im = ax.imshow(data, vmin=0, vmax=100, cmap='YlGnBu', aspect='auto')
    ax.set_xticks(range(len(columns)), [names[m] for m in columns], rotation=43, ha='right')
    ax.set_yticks(range(25), [f"{f['family_id']}  {f['family']} (n={f['n']})" for f in summary['by_family']])
    for i, f in enumerate(summary['by_family']):
        for j, m in enumerate(columns):
            ax.text(j, i, str(f['models'][m]['correct']), ha='center', va='center', fontsize=9,
                    color='white' if data[i, j] >= 63 else '#162d42')
    ax.set_title('Different strengths beneath the overall scores', loc='left', fontsize=18, pad=28)
    ax.text(0, 1.018, 'Labels: correct count. Color: family accuracy. * Added October 16; all other runs October 15.', transform=ax.transAxes)
    fig.colorbar(im, ax=ax, shrink=.6, pad=.02).set_label('Correct / planned (%)')
    fig.text(.30, .018, 'Same 1,136 text questions across 25 families. Dates: October 15 and 16, 2026 (Toronto).\nSingle-shot decisions; no tools, answer feedback or explicit reasoning trace.', fontsize=9, color='#45535c')
    fig.subplots_adjust(left=.30, bottom=.19, top=.94, right=.95)
    save(fig, 'family_accuracy')

    order = sorted(models, key=lambda m: models[m]['latency_first_all']['median_ms'])
    y = np.arange(len(order))
    fig, axes = plt.subplots(1, 2, figsize=(15, height), sharey=True)
    costs = [100 * models[m]['cost_all_attempts']['known_usd'] for m in order]
    medians = [models[m]['latency_first_all']['median_ms'] / 1000 for m in order]
    p95 = [models[m]['latency_first_all']['p95_ms'] / 1000 for m in order]
    axes[0].barh(y, costs, color='#18867d', height=.6)
    for i, m in enumerate(order):
        cost = models[m]['cost_all_attempts']
        calculated = cost.get('sources', {}).get('usage_times_published_tariff', 0)
        text = ('~' if calculated else '') + f'{costs[i]:.2f}c'
        if cost['missing_attempts']:
            text += f" + {cost['missing_attempts']} unknown"
        axes[0].text(costs[i] + .06, i, text, va='center', fontsize=9)
    axes[0].set_xlim(0, max(costs) * 1.55)
    axes[0].set_xlabel('US cents / actual 1,136-question run, including retries')
    axes[0].set_title('Cost: returned charges or labelled calculation', loc='left')
    axes[0].set_yticks(y, [names[m] for m in order])
    axes[1].barh(y, medians, color='#163e65', height=.6, label='Median')
    axes[1].scatter(p95, y, color='#c37c25', marker='D', s=30, label='p95')
    for i, value in enumerate(medians):
        axes[1].text(value + .025, i + .23, f'{value:.3f} s', va='top', fontsize=9)
    axes[1].set_xlim(0, max(p95) * 1.2)
    axes[1].set_xlabel('First-attempt connect-to-full-response seconds')
    axes[1].set_title('Same full-response timer; different services/dates', loc='left')
    axes[1].legend(frameon=False)
    axes[0].invert_yaxis()
    for ax in axes:
        ax.grid(axis='x', alpha=.17)
        ax.set_axisbelow(True)
    fig.suptitle(f'{len(models)} services: quality has to be read alongside cost and speed', x=.07, ha='left', fontsize=18, fontweight='bold')
    fig.text(.07, .025, '* Added October 16, 2026; original eleven tested October 15 (Toronto). Microsoft: OpenRouter/Azure; Nimble: Bespoke direct.\nAll 1,136 first attempts per model, including failures. New HTTPS connection and at most two concurrent requests/model.\n~ Nimble cost calculated from returned input-token usage and published tariff. Missing charges unknown. Mercury promotional tariff.', fontsize=9, color='#45535c')
    fig.subplots_adjust(left=.23, top=.9, bottom=.15, wspace=.18)
    save(fig, 'cost_and_speed')
    paths = sorted(DEST.glob('overall_*'))
    (SOURCE / 'graphics_integrity.json').write_text(json.dumps({
        'plotter_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'matplotlib_version': matplotlib.__version__,
        'source_summary_sha256': sha256((SOURCE / 'summary.json').read_bytes()).hexdigest(),
        'files_sha256': {p.name: sha256(p.read_bytes()).hexdigest() for p in paths}}, indent=2) + '\n')
    print('Built combined accuracy, family and cost/speed figures')


if __name__ == '__main__':
    main()
