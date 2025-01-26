from wordcloud import WordCloud # type: ignore
from dash import Dash, Input, Output, State, dcc, html # type: ignore
from collections import defaultdict
import base64
from io import BytesIO

# Initialisation de l'application Dash
app = Dash(__name__)

# Mise en page
app.layout = html.Div([
    html.H1("Système de recherche textuelle"),
    dcc.Input(id='search-input', type='text', placeholder='Entrez un mot ou une expression', style={'width': '60%'}),
    html.Button('Rechercher', id='search-button'),
    html.Div(id='results-output', style={'margin-top': '20px'})
])

# Fonction pour générer un Word Cloud
def generate_wordcloud(context_words):
    if not context_words:
        return ""

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(context_words))
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

# Fonction pour extraire des extraits de texte
def extract_contexts(expression, data, inverted_index):
    tokens = expression.lower().split()
    contexts = []
    context_words = []
    doc_indices = defaultdict(list)

    for doc_id, position in inverted_index.get(tokens[0], []):
        if all((doc_id, position + i) in inverted_index.get(tokens[i], []) for i in range(len(tokens))):
            token_list = data.iloc[doc_id]['tokens']
            start = max(0, position - 5)  # 5 mots avant l'expression
            end = position + len(tokens) + 5  # 5 mots après l'expression
            contexts.append(' '.join(token_list[start:end]))
            context_words += token_list[start:position] + token_list[position + len(tokens):end]
            doc_indices[doc_id].append(position)

    return contexts, context_words, doc_indices

# Fonction pour calculer les statistiques
def calculate_statistics(expression, doc_indices):
    total_appearances = sum(len(positions) for positions in doc_indices.values())
    mean_appearances = {doc_id: sum(positions) / len(positions) for doc_id, positions in doc_indices.items()}
    distribution = {doc_id: positions for doc_id, positions in doc_indices.items()}

    return total_appearances, mean_appearances, distribution

# Callback pour traiter la recherche
@app.callback(
    Output('results-output', 'children'),
    Input('search-button', 'n_clicks'),
    State('search-input', 'value')
)
def update_results(n_clicks, search_query):
    if n_clicks is None or not search_query:
        return "Entrez un mot ou une expression pour commencer la recherche."

    # Extraction des extraits et mots de contexte
    contexts, context_words, doc_indices = extract_contexts(search_query, data, inverted_index) # type: ignore

    if contexts:
        # Génération du Word Cloud
        wordcloud_src = generate_wordcloud(context_words)

        # Calcul des statistiques
        total_appearances, mean_appearances, distribution = calculate_statistics(search_query, doc_indices)

        # Affichage des extraits, Word Cloud et statistiques
        return html.Div([
            html.H3("Extraits de texte contenant l'expression :"),
            html.Ul([html.Li(context) for context in contexts]),
            html.H3("Word Cloud des mots de contexte :"),
            html.Img(src=wordcloud_src, style={'width': '80%', 'margin-top': '20px'}),
            html.H3("Statistiques :"),
            html.P(f"Nombre total d'apparitions : {total_appearances}"),
            html.H4("Distribution des indices dans les documents :"),
            html.Ul([html.Li(f"Document {doc_id} : {positions}") for doc_id, positions in distribution.items()]),
            html.H4("Moyenne d'apparition dans chaque document :"),
            html.Ul([html.Li(f"Document {doc_id} : {mean:.2f}") for doc_id, mean in mean_appearances.items()])
        ])
    else:
        return "Aucun résultat trouvé."

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
