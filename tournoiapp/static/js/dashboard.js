const niveauxLibelles = {
    1: "Débutant",
    2: "Amateur",
    3: "Semi-pro",
    4: "Pro",
    5: "Expert",
    6: "Légende"
};

document.addEventListener('DOMContentLoaded', () => {
    const modalAjouter = document.getElementById('modal-ajout-joueur');
    const modalModifier = document.getElementById('modal-modifier-joueur');
    const btnAjouter = document.getElementById('btn-ajouter-joueur');
    const formAjouter = document.getElementById('form-ajout-joueur');
    const formModifier = document.getElementById('form-modifier-joueur');
    const ul = document.getElementById('dashboard');

    const inputModifierId = document.getElementById('modifier-joueur-id');
    const inputModifierNom = document.getElementById('modifier-nom');
    const selectModifierNiveau = document.getElementById('modifier-niveau');

    // ---------- OUVRIR ----------
    btnAjouter.addEventListener('click', () => modalAjouter.classList.add('open'));

    // ---------- FERMER ----------
    [modalAjouter, modalModifier].forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('close')) {
                modal.classList.remove('open');
            }
        });
    });

    // ---------- AJOUTER JOUEUR ----------
    formAjouter.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = new FormData(formAjouter);

        const response = await fetch('/ajouter_joueur', { method: 'POST', body: data });
        if(response.ok){
            const joueur = await response.json();
            const li = document.createElement('li');
            li.dataset.id = joueur.id;
            li.innerHTML = `
                ${joueur.nom} <span class="badge badge-${joueur.niveau}">${niveauxLibelles[joueur.niveau]}</span>
                <button class="btn-modifier" title="Modifier">✏️</button>
                <button class="btn-supprimer" title="Supprimer">🗑️</button>
            `;
            ul.appendChild(li);
            modalAjouter.classList.remove('open');
            formAjouter.reset();
        } else {
            alert('Erreur lors de l’ajout du joueur.');
        }
    });

    // ---------- SUPPRIMER / MODIFIER ----------
    ul.addEventListener('click', (e) => {
        const li = e.target.closest('li');
        if(!li) return;
        const joueurId = li.dataset.id;

        // SUPPRIMER
        if(e.target.classList.contains('btn-supprimer')){
            if(!confirm('Voulez-vous vraiment supprimer ce joueur ?')) return;

            fetch(`/supprimer_joueur/${joueurId}`, {method: 'POST'})
                .then(resp => {
                    if(resp.ok) li.remove();
                    else alert('Erreur lors de la suppression.');
                });
        }

        // MODIFIER
        if(e.target.classList.contains('btn-modifier')){
            inputModifierId.value = joueurId;
            inputModifierNom.value = li.querySelector('.badge').previousSibling.textContent.trim();
            selectModifierNiveau.value = li.querySelector('.badge').className.match(/badge-(\d)/)[1];
            modalModifier.classList.add('open');
        }
    });

    // ---------- ENREGISTRER MODIFICATION ----------
    formModifier.addEventListener('submit', async (e) => {
        e.preventDefault();
        const joueurId = inputModifierId.value;
        const data = new FormData(formModifier);

        const response = await fetch(`/modifier_joueur/${joueurId}`, { method: 'POST', body: data });
        if(response.ok){
            const joueur = await response.json();
            const li = ul.querySelector(`li[data-id="${joueur.id}"]`);
            li.innerHTML = `
                ${joueur.nom} <span class="badge badge-${joueur.niveau}">${niveauxLibelles[joueur.niveau]}</span>
                <button class="btn-modifier" title="Modifier">✏️</button>
                <button class="btn-supprimer" title="Supprimer">🗑️</button>
            `;
            modalModifier.classList.remove('open');
        } else {
            alert('Erreur lors de la modification.');
        }
    });
});
