
export const print = (text)=>{

  window.printer.printDirect({
    data: window.iconv.convert(text),
    type:"text",
    success:function(jobID){
        console.log("sent to printer with ID: "+jobID);
      },
      error:function(err){
        console.log(err);
      }
})
}
