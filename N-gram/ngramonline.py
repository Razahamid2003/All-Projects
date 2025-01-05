import tiktoken
import streamlit as st

st.title("Text File Uploader and Reader with TikTokenizer")

uploaded_file = st.file_uploader("Choose a text file", type="txt")

content = ""  # Initialize content as an empty string

if uploaded_file is not None:
    # Read the file content
    content = uploaded_file.read().decode("utf-8")

if content:  # Proceed if content is not empty
    # Initialize the TikTokenizer
    enc = tiktoken.get_encoding("gpt2")  # Use "gpt2" encoding as an example

    # Tokenize the content
    tokens = enc.encode(content)

    # Convert tokens back to words for the N-gram model
    corpus = enc.decode(tokens).split()
    corpus_lower = [word.lower() for word in corpus]
    corpus_vocab = set(corpus_lower)
    corpus_vocab = list(corpus_vocab)

    n = st.text_input("Enter the value of N")
    N = int(n) if n.isdigit() else 1
    tokens_input = st.text_input("Enter the max number of tokens to generate")
    num_tokens = int(tokens_input) if tokens_input.isdigit() else 1

    N_gram = {}
    N_plus_1_gram = {}

    for i in range(len(corpus_lower) - N):
        N_gram_tuple = tuple(corpus_lower[i:i+N])
        N_plus_1_gram_tuple = tuple(corpus_lower[i:i+N+1])

        if N_gram_tuple in N_gram.keys():
            N_gram[N_gram_tuple] += 1
        else:
            N_gram[N_gram_tuple] = 1

        if N_plus_1_gram_tuple in N_plus_1_gram.keys():
            N_plus_1_gram[N_plus_1_gram_tuple] += 1
        else:
            N_plus_1_gram[N_plus_1_gram_tuple] = 1

    def generate_text(input_text, N, N_gram, N_plus_1_gram, corpus_vocab, num_tokens):
        words = input_text.split()

        for _ in range(num_tokens):
            if len(words) < N:
                next_word = "N/A"
            else:
                last_N_words = tuple(words[-N:])

                if last_N_words not in N_gram:
                    next_word = "N/A"
                else:
                    denominator = N_gram[last_N_words]

                    count = []
                    for word in corpus_vocab:
                        next_word_tuple = last_N_words + (word,)
                        if next_word_tuple in N_plus_1_gram:
                            count.append([word, N_plus_1_gram[next_word_tuple]])

                    prob_count = []
                    for word_count in count:
                        prob_count.append([word_count[1] / denominator, word_count[0]])

                    prob_count = sorted(prob_count, reverse=True)

                    next_word = prob_count[0][1] if prob_count else None

                    words.append(next_word)

        return ' '.join(words)

    input_text = st.text_input("Enter sample text")
    if input_text:
        result = generate_text(input_text, N, N_gram, N_plus_1_gram, corpus_vocab, num_tokens)
        st.write(result)
else:
    st.write("Please upload a text file.")
