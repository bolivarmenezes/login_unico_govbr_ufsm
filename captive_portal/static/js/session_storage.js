$(function() {
state = "pegar na url"
code_verifier = "pega na url também"
}
    function saveStateAndVerifier() {
      /*
      Don't overwrite our saved state if location has the state parameter.
      This means we got authorization from the AS, and we need to compare them later.
     */
      if (window.location.search.includes("state")) return;
      const storage = window.sessionStorage;
      storage.clear();
      storage.setItem("state", state);
      storage.setItem("code_verifier", code_verifier);
    }

    saveStateAndVerifier();
}