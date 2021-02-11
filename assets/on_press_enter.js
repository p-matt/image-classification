


setTimeout(function()
{ 
    document.getElementById("input").addEventListener("keyup", event => 
	{

		if(event.key !== "Enter") return; // Use `.key` instead.
		document.getElementById("sub").click(); // Things you want to do.
		event.preventDefault();
	});
 }, 3000);