const controls = document.getElementById('route-controls');
const team = document.getElementById('route-team');
const date = document.getElementById('route-date');
const channel = document.getElementById('route-channel');
const rows = [...document.querySelectorAll('#route-rows tbody tr')];
const title = document.getElementById('route-title');
const address = document.getElementById('route-address');
const subject = document.getElementById('route-subject');
const body = document.getElementById('route-body');

function previewReport() {
  const row = rows.find(candidate =>
    candidate.cells[0].textContent === team.value &&
    candidate.querySelector('time').dateTime === date.value
  );
  for (const candidate of rows) {
    candidate.classList.toggle('matched', candidate === row);
  }

  const day = date.selectedOptions[0].textContent;
  const email = channel.value === 'Email';
  address.hidden = !row;
  subject.hidden = !row || !email;
  if (!row) {
    title.textContent = date.value ? 'No matching report' : 'Choose a report date';
    body.textContent = date.value
      ? `Team ${team.value} has no report for ${day}. Choose a date listed for this team in the table.`
      : 'Choose a date to preview this team’s report.';
    return;
  }

  title.textContent = email ? 'Email preview' : 'Microsoft Teams preview';
  address.textContent = email ? `Email to the Team ${team.value} distribution list` : `Message to Team ${team.value}`;
  subject.textContent = email ? `Subject: Daily activity report for ${day}` : '';
  body.textContent = `Team ${team.value} completed ${row.cells[2].textContent} activities on ${day}.`;
}

controls.addEventListener('change', previewReport);
window.addEventListener('pageshow', previewReport);
previewReport();
controls.hidden = false;
