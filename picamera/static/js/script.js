
function toggleStream(streamId, url) {
  const checkbox = document.getElementById('checkbox' + streamId.slice(-1));
  const stream = document.getElementById(streamId);
  if (checkbox.checked) {
    stream.src = url;
    stream.style.display = 'block';
  } else {
    stream.src = '';
    stream.style.display = 'none';
  }
}

// function

function startup() {
  fetch('http://127.0.0.1/startup', {
    method: 'POST'
  }).then((response) => {
    console.log(response)
  });

}

function kill() {
  fetch('http://127.0.0.1/killCameras', {
    method: 'POST'
  });
}

function getCams() {
  
}