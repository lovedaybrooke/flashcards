function respond() {

  var result = event.srcElement.closest(".answer-card").id

  var buttonDiv = document.getElementsByClassName("slanted-button");
  buttonDiv[0].style.display = 'block';

  var answerCard = document.getElementsByClassName("answer-card").namedItem(result);
  answerCard.classList.remove("answer-concealed");

  const xhr = new XMLHttpRequest();
  var postURL = "/learn/" + document.getElementById("learner_id").innerText
  var FD  = new FormData();
  FD.append( "question_type", document.getElementById("question-type").innerText );
  FD.append( "combination_id", document.getElementById("combination").innerText );
  FD.append( "result", result );

  xhr.open('POST', postURL);
  xhr.send( FD );  
}