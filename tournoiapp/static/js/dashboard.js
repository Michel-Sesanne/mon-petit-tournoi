const niveauxLibelles = {
    1: "Débutant",
    2: "Amateur",
    3: "Semi-pro",
    4: "Pro",
    5: "Expert",
    6: "Légende"
};

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal-ajout-joueur');
    const btn = document.getElementById('btn-ajouter-joueur');
    const spanClose = modal.querySelector('.close');
    const form = document.getElementById('form-ajout-joueur');
    const ul = document.getElementById('dashboard');

    // Ouvrir modale
    btn.onclick = () => modal.style.display = 'flex';

    // Fermer modale
    spanClose.onclick = () => modal.style.display = 'none';
    window.onclick = (event) => { if(event.target === modal) modal.style.display = 'none'; }

    // Soumission AJAX
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const data = new FormData(form);

        const response = await fetch('/ajouter_joueur', {
            method: 'POST',
            body: data
        });

        if(response.ok) {
            const joueur = await response.json();
            const li = document.createElement('li');
            li.innerHTML = `${joueur.nom} <span class="badge badge-${joueur.niveau}">${niveauxLibelles[joueur.niveau] || "Inconnu"}</span>`;

            ul.appendChild(li);
            modal.style.display = 'none';
            form.reset();
        } else {
            alert('Erreur lors de l’ajout du joueur.');
        }
    });
});
