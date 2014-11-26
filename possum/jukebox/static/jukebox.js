var intervId;
var intervFin;
var infos;

String.prototype.toMMSS = function () {
	var sec_num = parseInt(this, 10);
	var minutes = Math.floor(sec_num / 60);
	var seconds = sec_num - (minutes * 60);

	if (minutes < 10) {minutes = "0"+minutes;}
	if (seconds < 10) {seconds = "0"+seconds;}
	var time    = minutes+':'+seconds;
	return time;
}

function setinfos()
{
	$.get('ajax/info', function( data ) {
		  infos = $.parseJSON(data);
		  $("pre#song").html(infos.song);
		  $("pre#artist").html(infos.artist);
		  $("pre#time").html(infos.elapsed.toMMSS()+"/"+infos.time.toMMSS());
		  $( "progress#progressbar" ).attr('value',parseFloat(infos.elapsed)/parseFloat(infos.time)*100);
		  clearInterval(intervId);
		  clearInterval(intervFin);
		  if(infos.status=="play") {
		  	// refresh at every more 7% played
		  	intervId = setInterval(setinfos, parseFloat(infos.time)/100*7*1000);
			// refresh when next song starts to play
		  	intervFin = setInterval(setinfos, (parseFloat(infos.time)-parseFloat(infos.elapsed)+1)*1000);
		  	console.log("Refresh every (s) : " + parseFloat(infos.time)/100*7);
		  	console.log("Next song (s) : " + (parseFloat(infos.time)-parseFloat(infos.elapsed)+1));
		  }
		});
}

$("button#play").click(ajaxplay);
$("button#pause").click(ajaxpause);
$("button#next").click(ajaxnext);
$("button#previous").click(ajaxprevious);
$("button#remove").click(ajaxremove);

function ajaxplay()
{
  ajaxfunct('play');
  return false;
}

function ajaxpause()
{
  ajaxfunct('pause');
  clearInterval(intervId);
  clearInterval(intervFin);
  console.log("paused");
  return false;
}

function ajaxfunct(strfunct)
{
	$.ajax({
		url: 'ajax/'+strfunct,
		type : 'GET'
	});
	setinfos();
	return false;
}

function ajaxnext()
{
  ajaxfunct('next');
}

function ajaxprevious()
{
	ajaxfunct('previous');
}

function ajaxremove()
{
	ajaxfunct('remove');
}

$(document).ready(function(){
	setinfos();
	$("input#subbtn").remove();
	$("select#id_pl").change(function(){
		$.ajax({
		url: 'ajax/play',
		type : 'GET',
		data : "pl="+$("select#id_pl").val()
	    });
	    setinfos();
	});
});
