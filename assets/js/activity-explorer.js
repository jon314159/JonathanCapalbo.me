(() => {
  'use strict';
  const host = document.getElementById('activity-explorer-root');
  const fallback = document.getElementById('activity-explorer-fallback');
  const status = document.getElementById('activity-explorer-status');
  const retry = document.getElementById('activity-explorer-retry');
  if (!host || !fallback || !status || !retry) return;
  const products = ['Core Package', 'Plus Package', 'Premium Package', 'Optional Add-on'];
  const outcomes = ['Completed', 'Follow-up', 'No sale'];
  const short = {'Core Package': 'Core', 'Plus Package': 'Plus', 'Premium Package': 'Premium', 'Optional Add-on': 'Add-on'};
  const fields = ['Date', 'Time', 'Interaction ID', 'Product', 'Outcome', 'Units', 'Points', 'Follow-up', 'Notes', 'Original row'];
  const dateLabel = date => `Jul ${Number(date.slice(8))}`;
  const pct = value => `${(value * 100).toFixed(1)}%`;
  const total = (rows, field) => rows.reduce((sum, row) => sum + row[field], 0);
  let root;

  function validate(data) {
    if (data.schemaVersion !== 1 || data.fictional !== true || !Array.isArray(data.rows) || data.rows.length !== 465) throw new Error('Unexpected dataset');
    const ids = new Set();
    for (const row of data.rows) {
      if (!fields.every(field => Object.hasOwn(row, field)) || !/^2026-07-(0[1-9]|[12]\d|3[01])$/.test(row.Date)
        || !/^FAKE-/.test(row['Interaction ID']) || ids.has(row['Interaction ID']) || !products.includes(row.Product)
        || !outcomes.includes(row.Outcome) || !Number.isInteger(row.Units) || row.Units < 0 || !Number.isFinite(row.Points)) throw new Error('Invalid record');
      ids.add(row['Interaction ID']);
    }
    if (total(data.rows, 'Units') !== 324 || total(data.rows, 'Points') !== 402.5
      || data.rows.filter(row => row.Outcome === 'Completed').length !== 282) throw new Error('Totals do not reconcile');
    return data;
  }

  function Explorer({data}) {
    const h = React.createElement;
    const [target, setTarget] = React.useState(11);
    const [product, setProduct] = React.useState('All products');
    const [outcome, setOutcome] = React.useState('All outcomes');
    const [day, setDay] = React.useState('All days');
    const [mark, setMark] = React.useState(null);
    const [page, setPage] = React.useState(0);
    const rows = data.rows;
    const completed = rows.filter(row => row.Outcome === 'Completed');
    const daily = React.useMemo(() => Array.from({length:31}, (_, i) => {
      const date = `2026-07-${String(i + 1).padStart(2, '0')}`;
      const records = rows.filter(row => row.Date === date);
      const done = records.filter(row => row.Outcome === 'Completed');
      return {date, activities: records.length, completed: done.length, units:total(done, 'Units'), share:done.length / records.length, per:total(done, 'Units') / done.length};
    }), [rows]);
    const subset = rows.filter(row => (product === 'All products' || row.Product === product) && (outcome === 'All outcomes' || row.Outcome === outcome));
    const records = subset.filter(row => (day === 'All days' || row.Date === day) && (!mark || (row.Product === mark.product && row.Outcome === mark.outcome)));
    const pageSize = 10;
    const pages = Math.max(1, Math.ceil(records.length / pageSize));
    const currentPage = Math.min(page, pages - 1);
    const visible = records.slice(currentPage * pageSize, (currentPage + 1) * pageSize);
    const met = daily.filter(item => item.units >= target).length;
    const change = setter => event => {setter(event.target.value); setPage(0);};
    const clear = () => {setDay('All days'); setMark(null); setPage(0);};
    const reset = () => {clear(); setProduct('All products'); setOutcome('All outcomes'); setTarget(11);};
    const button = (text, action, props = {}) => h('button', {type:'button', onClick:action, ...props}, text);
    const select = (label, id, value, choices, setter) => h('label', {htmlFor:id}, label, h('select', {id, value, onChange:change(setter)}, choices.map(choice => h('option', {key:choice, value:choice}, choice))));
    const scope = `${product}; ${outcome}; ${day === 'All days' ? 'all dates' : dateLabel(day)}${mark ? `; chart selection: ${short[mark.product]} ${mark.outcome}` : ''}`;

    function Chart({title, measure, maximum, format, bar = false, reference = false}) {
      const width = 620, height = 210, left = 0, right = 0, top = 2, bottom = 2;
      const plotWidth = width - left - right, plotHeight = height - top - bottom;
      const x = index => left + (index + .5) * plotWidth / 31;
      const y = value => top + plotHeight * (1 - value / maximum);
      const path = daily.map((item, index) => `${index ? 'L' : 'M'}${x(index)},${y(item[measure])}`).join(' ');
      return h('figure', {className:'activity-chart'},
        h('figcaption', null, h('strong', null, title), h('span', null, 'All 31 days · All products and outcomes')),
        h('div', {className:'activity-chart-plot'},
          h('div', {className:'activity-y-axis', 'aria-hidden':'true'}, [maximum, maximum / 2, 0].map(value => h('span', {key:value}, format(value)))),
          h('svg', {viewBox:`0 0 ${width} ${height}`, preserveAspectRatio:'none', role:'img', 'aria-label':`${title}. July 1 through 31, 2026. Scale zero to ${format(maximum)}. Exact values and day selection are in the daily values table.`},
          [0, maximum / 2, maximum].map(value => h('line', {key:value, x1:left, x2:width-right, y1:y(value), y2:y(value), className:'activity-gridline'})),
          reference && h('line', {x1:left, x2:width-right, y1:y(target), y2:y(target), className:'activity-target-line'}),
          bar ? daily.map((item, index) => h('rect', {key:item.date, x:x(index)-6, y:y(item[measure]), width:12, height:top+plotHeight-y(item[measure]), fill:reference && item.units < target ? '#8b4f0a' : '#315eea'}))
            : h('path', {d:path, className:'activity-trend'})),
          h('div', {className:'activity-x-axis', 'aria-hidden':'true'}, [0, 15, 30].map(index => h('span', {key:index}, dateLabel(daily[index].date))))),
        reference && h('p', {className:'activity-chart-note'}, `${met} Met · ${31 - met} Below. The dashed line marks ${target} units/day. Read each day’s status in the table below.`));
    }

    return h('div', {className:'activity-explorer', onKeyDown:event => {if (event.key === 'Escape') clear();}},
      h('div', {className:'activity-month-summary', 'data-testid':'month-summary'},
        h('p', null, h('strong', null, '465'), ' activities'), h('p', null, h('strong', null, '282'), ' completed interactions'),
        h('p', null, h('strong', null, '324'), ' completed units'), h('p', null, h('strong', null, '402.5'), ' points'),
        h('p', null, h('strong', null, pct(completed.length / rows.length)), ' completed-interaction share'),
        h('p', null, h('strong', null, (total(completed, 'Units') / completed.length).toFixed(2)), ' units per completed interaction')),
      h('p', {className:'activity-scope-note'}, 'Month totals and daily charts always use all 465 source records. Product and outcome controls narrow the outcome table and records. Chart and day selections narrow records only.'),
      h('div', {className:'activity-controls'},
        select('Daily unit target', 'activity-target', String(target), Array.from({length:26}, (_, i) => String(i)), value => setTarget(Number(value))),
        select('Product', 'activity-product', product, ['All products', ...products], setProduct),
        select('Outcome', 'activity-outcome', outcome, ['All outcomes', ...outcomes], setOutcome),
        h('label', {htmlFor:'activity-day'}, 'Inspect day (records only)', h('select', {id:'activity-day', value:day, onChange:change(setDay)}, h('option', {value:'All days'}, 'All days'), daily.map(item => h('option', {key:item.date, value:item.date}, dateLabel(item.date))))),
        h('div', {className:'activity-reset-controls'}, button('Clear chart selection', clear, {disabled:day === 'All days' && !mark}), button('Reset all controls', reset))),
      h('p', {className:'activity-target-summary', role:'status', 'data-testid':'target-summary'}, `${met} Met / ${31} days at ${target} units/day; ${31 - met} Below. This target implies ${target * 31} units over July. Monthly product goals total 310 units and remain separate.`),
      h('section', {className:'activity-outcomes', 'aria-labelledby':'activity-outcomes-title'},
        h('h3', {id:'activity-outcomes-title'}, 'Outcomes by product'),
        h('p', null, `${subset.length} interactions in the product/outcome subset. Select a count to inspect those records.`),
        h('table', {className:'activity-outcome-table'}, h('caption', null, 'Interaction counts; product and outcome controls apply'),
          h('thead', null, h('tr', null, h('th', {scope:'col'}, 'Product'), ...outcomes.map(value => h('th', {scope:'col', key:value}, value)))),
          h('tbody', null, products.filter(value => product === 'All products' || product === value).map(value => h('tr', {key:value},
            h('th', {scope:'row'}, short[value]), ...outcomes.map(result => {
              const count = subset.filter(row => row.Product === value && row.Outcome === result).length;
              return h('td', {key:result, 'data-label':result}, button(String(count), () => {setMark({product:value, outcome:result}); setPage(0);}, {'aria-label':`Inspect ${short[value]} ${result}: ${count} interactions`, 'aria-pressed':Boolean(mark && mark.product === value && mark.outcome === result)}));
            })))))) ,
      h(Chart, {title:'Daily completed units', measure:'units', maximum:Math.max(20, target), format:value => String(value), bar:true, reference:true}),
      h('div', {className:'activity-diagnostics'},
        h(Chart, {title:'Daily activity volume', measure:'activities', maximum:20, format:value => String(value), bar:true}),
        h(Chart, {title:'Completed-interaction share', measure:'share', maximum:1, format:value => `${Math.round(value * 100)}%`}),
        h(Chart, {title:'Units per completed interaction', measure:'per', maximum:2, format:value => value.toFixed(1)})),
      h('details', {className:'activity-daily-values'}, h('summary', null, 'Read daily values and inspect a day'),
        h('table', null, h('caption', null, 'July 2026, all products and outcomes; status uses the selected daily target'),
          h('thead', null, h('tr', null, ...['Day', 'Activities', 'Completed', 'Units', 'Status', 'Completed share', 'Units per completed'].map(value => h('th', {scope:'col', key:value}, value)))),
          h('tbody', null, daily.map(item => h('tr', {key:item.date}, h('th', {scope:'row'}, button(dateLabel(item.date), () => {setDay(item.date); setPage(0);}, {'aria-label':`Inspect records for ${dateLabel(item.date)}`, 'aria-pressed':day === item.date})),
            ...[['Activities', item.activities], ['Completed', item.completed], ['Units', item.units], ['Status', item.units >= target ? 'Met' : 'Below'], ['Completed share', pct(item.share)], ['Units per completed', item.per.toFixed(2)]].map(([label, value]) => h('td', {key:label, 'data-label':label}, value))))))),
      h('section', {className:'activity-records', 'aria-labelledby':'activity-records-title'},
        h('h3', {id:'activity-records-title'}, 'Fictional records'),
        h('p', {role:'status', 'aria-atomic':'true', 'data-testid':'record-count'}, `${records.length} matching records. ${scope}.`),
        records.length === 0 ? h('div', {className:'activity-empty'}, h('p', null, 'No records match these controls and selections. Clear chart selection to return to the product/outcome subset, or reset all controls for all 465 records.')) :
          h('table', {className:'activity-record-table'}, h('caption', null, `Records ${currentPage * pageSize + 1}–${Math.min((currentPage + 1) * pageSize, records.length)} of ${records.length}; open Details for all 10 source fields`),
            h('thead', null, h('tr', null, ...['ID', 'Date', 'Product', 'Outcome', 'Units', 'Points', 'Details'].map(value => h('th', {scope:'col', key:value}, value)))),
            h('tbody', null, visible.map(row => h('tr', {key:row['Interaction ID']}, h('th', {scope:'row'}, row['Interaction ID']),
              ...[['Date', dateLabel(row.Date)], ['Product', short[row.Product]], ['Outcome', row.Outcome], ['Units', row.Units], ['Points', row.Points]].map(([label, value]) => h('td', {key:label, 'data-label':label}, value)),
              h('td', {'data-label':'Details'}, h('details', null, h('summary', {'aria-label':`Details for ${row['Interaction ID']}`}, 'Details'), h('dl', {className:'activity-record-detail'}, fields.map(field => h('div', {key:field}, h('dt', null, field === 'Original row' ? 'Source row' : field), h('dd', null, String(row[field]))))))))))),
        h('div', {className:'activity-pagination'}, button('Previous records', () => setPage(currentPage - 1), {disabled:currentPage === 0}), h('span', null, `Page ${currentPage + 1} of ${pages}`), button('Next records', () => setPage(currentPage + 1), {disabled:currentPage >= pages - 1}))),
      h('p', {className:'activity-scope-note'}, 'Follow-up is a recorded activity flag, not an unresolved backlog. These fictional records do not establish causes, response times, revenue, or improvement. Dates are reporting dates in July 2026.'));
  }

  function fail() {
    status.textContent = 'The interactive view could not load. The static totals, Tableau preview, and downloads remain available. Retry the browser view to try again.';
    status.hidden = false;
    retry.hidden = false;
    fallback.hidden = false;
    host.hidden = true;
  }

  async function load() {
    status.hidden = false;
    status.textContent = 'Loading the fictional activity records…';
    retry.hidden = true;
    if (!window.React || !window.ReactDOM) {fail(); return;}
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch('assets/data/fictional-activities.json', {signal:controller.signal});
      if (!response.ok) throw new Error('Dataset unavailable');
      const data = validate(await response.json());
      if (!root) root = ReactDOM.createRoot(host);
      class Boundary extends React.Component {
        constructor(props) {super(props); this.state = {failed:false};}
        static getDerivedStateFromError() {return {failed:true};}
        componentDidCatch() {fail();}
        render() {return this.state.failed ? null : this.props.children;}
      }
      root.render(React.createElement(Boundary, {key:Date.now()}, React.createElement(Explorer, {data})));
      host.hidden = false;
      fallback.hidden = true;
      status.hidden = true;
    } catch {fail();} finally {clearTimeout(timeout);}
  }
  retry.addEventListener('click', load);
  load();
})();
