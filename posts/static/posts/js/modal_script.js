var shareModal = document.getElementById('shareModal')
shareModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var post_id = button.getAttribute('data-bs-whatever')

    const BASE_URL = "https://campusphere.cs-campus.fr/"; 

    const whatsappLink = document.getElementById("whatsapp_link");
    whatsappLink.href = getWhatsappShareLink(post_id, BASE_URL);

    const telegramlink = document.getElementById("telegram_link");
    telegramlink.href = getTelegramShareLink(post_id, BASE_URL);
})


function getWhatsappShareLink(id, BASE_URL) {
  
    // Initialize the WhatsApp URL
    const wa_url = "https://api.whatsapp.com/send?text=";
  
    // Create the link to the post
    const link_to_post = BASE_URL + "posts/" + id + "/show/";
  
    // Create the explanatory text
    const texte_explicatif = "Viens donner ton avis ! ";
  
    // Return the final WhatsApp share link
    return wa_url + encodeURIComponent(texte_explicatif) + encodeURIComponent(link_to_post);
}
  
function getTelegramShareLink(id, BASE_URL) {
      
     // Create the link to the post
     const link_to_post = BASE_URL + "posts/" + id + "/show/";
      
     // Return the final Telegram share link
     return "https://t.me/share/url?url=" + encodeURIComponent(link_to_post) + "&text=" + encodeURIComponent("Viens donner ton avis ! ");
    }