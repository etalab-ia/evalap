import json
import re
from evalap.clients import LlmClient, split_think_answer
from evalap.utils import render_jinja

from . import metric_registry

_template = """
Vous êtes un assistant administratif, expert dans l'analyse de questions et leurs complexités.
Voilà la question à analyser :

{{query}}

Évaluez la demande selon ces critères administratifs :

1. Clarté de la demande : La question est simple, claire et précise. Elle traite d'un sujet unique.
2. Nombre d'administrations impliquées : La question réfère à une seule administration (ex : CAF) ou bien à plusieurs en même temps
3. Complexité des procédures requises : La réponse à la question va être simple ou bien complexe. Elle nécessite une seule source pour y répondre ou plusieurs? ...

Pour chaque score, plus la note est élevée, plus la question/demande est complexe.

Pour chaque critère :
- Donnez une brève explication (1-2 phrases)
- Notez-le sur une échelle de 1 à 5 (1 étant le plus simple, 5 le plus complexe)

Format de réponse attendu :

Critère Demande : [Explication] [Note : X/5]
Critère Administration : [Explication] [Note : X/5]
Critère Procedure : [Explication] [Note : X/5]
Score de complexité global : [Explication] [Note : X/10]
Attention, si vous ne savez pas donner de note, mettre 0! ne jamais laisser la note vide
Recommandation : [Suggérez brièvement la marche à suivre pour traiter cette demande]

Enfin, vous nous direz quelle est la thématique principale associée à cette demande administrative parmis une liste de thème;
Liste des thèmes : CAF / ANTS / CPAM / CARSAT - MSA / IMPOTS / ...

si vous ne savez pas la classer, vous la mettrez dans la catégorie "non catégorisé"
Vous ajouterez cela à la réponse en mettant "thèmathique : [thème identifié]"

A vous.
""".strip()

_config = {
    "model": "gpt-4o",
    # "system_prompt": "Tu donnes...."
    "sampling_params": {"temperature": 0.2},
}


@metric_registry.register(
    name="judge_complexity",
    description="[0-10] La métrique 'judge_complexity' évalue la complexité d'une demande administrative selon sa clarté, le nombre d'administrations impliquées, et la complexité des procédures nécessaires. Elle sert à identifier la difficulté globale d’une question pour mieux orienter la prise en charge et les ressources à mobiliser. Cette métrique est utile pour prioriser les demandes simples ou complexes dans un cadre administratif.",
    metric_type="dataset",
    require=["query"],
)
def judge_complexity_metric(output, output_true, **kwargs):
    config = _config | {k: v for k, v in kwargs.items() if k in _config}
    messages = [
        {
            "role": "user",
            "content": render_jinja(_template, output=output, output_true=output_true, **kwargs),
        }
    ]
    model = config["model"]
    aiclient = LlmClient(base_url=model.base_url, api_key=model.api_key)
    result = aiclient.generate(model.name, messages=messages, **config["sampling_params"])
    observation = result.choices[0].message.content
    think, answer = split_think_answer(observation)

    def extract_score(line):
        match = re.search(r"\[Note : (\d+(?:\.\d+)?)/\d+\]", line)
        return float(match.group(1)) if match else 0

    scores = {"demande": 0, "administration": 0, "procedure": 0, "global": 0}

    thematique = "non catégorisé"

    for line in answer.split("\n"):
        if "Critère Demande :" in line:
            scores["demande"] = extract_score(line)
        elif "Critère Administration :" in line:
            scores["administration"] = extract_score(line)
        elif "Critère Procedure :" in line:
            scores["procedure"] = extract_score(line)
        elif "Score de complexité global :" in line:
            scores["global"] = extract_score(line)
        elif line.startswith("Thématique :"):
            thematique = line.split(":", 1)[1].strip()

    observation_ = {"answer": answer, "think": think, "scores": scores, "thematique": thematique}

    return int(scores["global"]), json.dumps(observation_), result
