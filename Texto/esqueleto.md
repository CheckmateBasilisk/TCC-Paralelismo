<!-- converting:

subseções
find: ^## (.*)
replace: \\section{$1}

italico
find: \*([^\*]+)\*[^\*]
replace: \\emph{$1}
bug: se o itálico chegar no final da linha dá ruim asuhus

negrito
find: \*\*([^\*]+)\*\*[^\*]
replace: \\textbf{$1}}

 -->

# TCC

## Introdução

- descrever a premissa e motivação
- descrever o que foi feito
- descrever brevemente os resultados
- tldr da conclusão

Pretendia-se abordar Haskell por ser uma linguagem funcional poderosa com um compilador robusto e intrincado, mas não houve tempo hábil para tal. Teria sido uma inclusão interessante, não somente pela mudança de paradigma, mas pelo fato de haskell possuir dados imutáveis por padrão e aprender essa linguagem quase taumatúrgica seria um experimento interessante. Basta dizer que para os "não iniciados", haskell é no mínimo esotérico e arcano. Também seria uma adição interessante pela comparação de desempenho, já que há o mito de que Haskell não consegue competir com linguagens mais tradicionais, apesar de ser compilado.


## Contextualização Teórica

Neste capítulo serão abordados termos e conceitos centrais ao tema tratado: a diferença entre Paralelismo e Concorrência (seção xx), alguns problemas comuns que atormentam programadores que enfrentam algoritmos paralelos (seção xx), algumas ferramentas clássicas utilizadas para sincronizar e paralelizar algoritmos (seção xx), alguns dos modelos de paralelismo (seção xx) em especial os utilizaos pelas linguagens estudadas: Python, Go, Kotlin e Rust.

### Motivação: Limites Físicos da Lei de Moore

É inegável a importância da computação para a civilização humana moderna. É sabido também que a demanda por poder computacional vem crescendo vertiginosamente (em inúmeras áreas, desde a academia ao entretenimento) e até recentemente a microeletrônica foi capaz de acompanhar, reduzindo o tamanho dos componentes (em especial transistores) e produzindo chips cada vez mais complexos e poderosos. As maiores maravilhas da ciência dos últimos séculos cabem em uma miúda caixa de aço e silício em nossos bolsos, mas a tendência de incrementar mais e mais os processadores e chips está chegando em seu limite.

A Lei de Moore, postulada por Gordon E. Moore em 1965 e revisada em 1975 (TODO: CITAÇÃO), afirma que a cada dois anos a densidade de transistores dobraria, fazendo crescer consigo a potência dos dispositivos. Não é surpresa que eventualmente um limite superior seria atingido sem uma mudança radical de paradigma. Dentre as razões estão: a imensa complexidade da microeletrônica envolvida, a impossibilidade de se resfriar os componentes e, surpreendentemente, o tunelamento dos elétrons entre os componentes, destruindo os dados.

Com tais limitações físicas em mente, abordagens outrora típicas de ficção científica vem sendo estudadas, como super materiais com características estranhas e computação quântica. Contudo, por agora, a melhor solução para a definhante Lei de Moore é adaptar e refinar a tecnologia existente, desenvolvendo as áreas de computação distribuída e computação paralela.

Um novo modo de programar demanda novas ferramentas e traz consigo novos desafios.

### Concorrência e Paralelismo

Baseado nas definições trazidas por Peter Pacheco (ref: pacheco p.09), podemos definir concorrência como o trabalho sobre múltiplas tarefas por um mesmo agente, alternadamente. Ou seja, certos passos das múltiplas tarefas são intercalados uns com os outros e se faz progresso em todas.

Uma analogia: Um estudante deseja passar em uma disciplina da graduação (cálculo 3) e resolve apelar para a superstição, confeccionando 1000 tsurus (pequenas dobraduras de cegonhas). Se fizesse uma a uma, do começo ao fim, trataria-se de uma abordagem sequencial (ou serial). O estudante decide fazer os tsurus parcialmente e depois retomar e terminar as dobraduras incompletas pois julga que será menos tedioso. Esta é uma abordagem concorrente (um agente alternando entre várias tarefas, iguais neste exemplo).

Paralelismo, por outro lado, demanda simultaneidade dos passos das diversas tarefas por diversos agentes. Os passos não são intercalados e as tarefas são desenvolvidas simultaneamente (mas não necessariamente sincronizadas ou emparelhadas, se forem tarefas iguais).

Retomando a analogia: Os amigos do estudante também estão com dificuldades e resolvem ajudar para receberem boa sorte. Cada um pega um punhado de papéis de dobradura e fazem, ao mesmo tempo, os tsurus. Alguns são mais rápidos e outros demoram mais para aprender, então neste exemplo o desenvolvimento das tarefas acontece em ritmos diferentes.

De acordo com esta definição um sistema que admite paralelismo, como o grupo de alunos como um todo, é necessariamente concorrente, ou seja, mesmo que cada agente que faz parte do grupo desempenhe suas tarefas sequencialmente, o grupo desempenha tarefas concorrentemente. Quando se trata de computadores, costuma-se chamar cada um desses agentes de **thread**.

<!-- TODO: FAZER UMA SEÇÃO SOBRE A LEI DE AMDAHL livro do peter pacheco -->
<!-- TODO: FAZER UMA SEÇÃO SOBRE O CONCEITO DE SPEEDUP -->
<!-- remover no overleaf
citação no lateX são referências a um segundo arquivo .bib com as referências completas e tal
abnt.sty é um arquivo de estilos que descreve como produzir as referências


\bibliographystyle{abnt}
\bibliography{refs.bib}
\end{document}


no overleaf

\cite{pachenko11}

% isso aqui no final
\bibliographystyle{apalike}
\bibliography{refs.bib}
 -->

### Speedup e Lei de Amdahl

 Praticamente todos os algorimos possuem seções sequenciais, nem que sejam somente o início e o fim (como os casos estudados nos experimentos, chamados trivialmente paralelizáveis ou embaraçosamente paralelizáveis (ref: pacheco p.48)).

Uma seção do algoritmo é dita sequencial se seus passos dependem dos resultados uns dos outros. Na analogia do estudante e seus tsurus: cada uma das dobras deve ser feita em sequência. Não faz sentido detalhar o bico da ave se o pescoço ainda nem foi dobrado.

O fator de redução do tempo gasto para desempenhar uma tarefa através de um novo algoritmo (paralelizando-o, nesse caso) é chamado de speedup. Em um computador ideal, pode-se dizer que o ganho de eficiência é limitado somente pelas seções sequenciais do algoritmo. Na prática isso não ocorre pois a cada nova thread criada há o esforço de gerenciamento de recursos e eventual destruição das threads impossibilitando o comportamento assintótico do speedup quando se aumenta o número de threads. Na analogia do estuadnte e seus tsurus: se conseguisse que o campus todo contribuísse (1000 alunos) e cada um fizesse um único tsuru, a tarefa ainda demoraria o tempo necessário para fazer uma dobradura (seção sequencial). O milésimo-primeiro aluno não seria capaz de acelerar o processo dos outros.

Outro exemplo muito comum e ironizado é a gravidez típica, que necessariamente dura 9 meses. Duas pessoas são incapazes de entregar um bebê em quatro meses e meio.

A Lei de Amdahl (TODO: REFERÊNCIA) formaliza o speedup máximo obtido em um programa:

\begin{equation}
    S_{latency} \left ( s \right ) = \frac{1}{\left ( 1 - p\right )+ \frac{p}{s}}
\end{equation}



Percebe-se que se o speedup s da seção paralelizável tender ao infinito (com infinitas threads, por exemplo), o tempo total de execução do algoritmo tende à soma das seções sequenciais. Na prática, o custo combinado do gerenciamento das threads cresce junto co o número de threads, produzindo um ponto de mínimo no qual o ganho é máximo em comparação ao incremento.

### Problemas Comuns de Algoritmos Paralelos

A paralelização de algoritmos nem sempre é trivial. Além de certos trechos não serem paralelizáveis, durante a execução não há garantias acerca da ordem de execução dos passos entre threads, ou seja, não há garantias de que uma thread alcança um certo ponto do algoritmo antes da outra, comprometendo a integridade dos resultados. Serão abordados alguns dos problemas mais comuns de algortimos paralelos a seguir.

#### Corrida, Atomicidade e Seções Críticas

Quando duas threads estão sendo executadas simultaneamente e compartilham uma variável, é possível que ambas tentem acessar o valor ao mesmo tempo (ou uma acesse o valor antes que a outra termine de atualizá-lo). Desse modo, o resultado depende de qual thread acessa a variável primeiro, corrompendo o resultado e tornando-o incerto. Chamamos isso de **condição de corrida** (ref: pacheco p.51). Quaisquer seções de código sucetíveis a condições de corrida e demandam que uma única thread acesse um dado recurso são chamadas **seções críticas** (ref. pacheco p.51).

Pode-se extender a definição de seção crítica para códigos concorrentes mantendo em mente a ideia de atomicidade: se há dependência direta do resultado de uma computação (leitura ou escrita inclusos), então é imperativo que nenhum outro processo, paralelo ou concorrente, utilize os valores atuais antes que tal computação seja concluída, ou seja, a computação deve ser **atômica**, indivisível, e em caso de concorrência ininterruptível (já que tentativas de acesso não podem ser simultâneas).

<!-- atomicidade tem a ver com threads (acesso simultâneo não rola, precisa de um gargalo) e processos (não deve ser desescalonado) -->

<!--
todo problema de concorrência é carregado pra paralelismo? tem cara de que sim!

A relação entre paralelismo e concorrência descrita acima alude à ...
-->

#### Atomicidade e Seções Críticas

Caso duas ou mais threads compartilhem uma mesma variável, é necessário garantir a atomicidade das operações sobre ela, ou seja, deve-se garantir que o scheduler não interrompa a operação e que outras threads aguardem sua vez. Um exemplo clássico é o de um contador incrementado por diversas threads: se não houver garantia que a leitura, incremento e escrita sejam, juntas, ininterruptíveis, várias threads incrementarão o mesmo valor e escreverão o mesmo valor, perdendo iterações e corrompendo o resultado final.

Chama-se um conjunto de operações sequenciais que não se pode interromper com segurança de Seções Críticas, e Mutexes são o mecanismo mais comum para garantir a atomicidade (serão descritas adiante).

#### Sincronização, Esperas e Travas

Existem mecanismos que permitem que threads esperem umas pelas outras, aguardando sinais e variáveis de controle que indicam que podem seguir adiante com suas tarefas. Costuma ser necessário, por exemplo, que uma thread aguarde a conclusão de várias outras e agregue todos os resultados antes de seguir adiante, ou que um recurso termine de ser utilizado para evitar condições de corrida.

Em suma: threads que devem aguardar resultados ou estados de outras threads devem ser **sincronizadas**, como na computação sobre um valor obtido de uma outra thread. Uma thread acessando recursos compartilhados (que não sejam read-only) devem **travar** outras threads enquanto os utiliza, como uma computação qualquer sobre uma variável compartilhada.

#### Deadlocks

Se mecanismos de trava forem utilizados, pode-se evitar condições de corrida, mas igualmente desastrosas são as situações de travamento mútuo chamado **deadlock**. É possível que dois processos, paralelos ou concorrentes, aguardem a liberação um recurso bloqueado pelo outro, ficando permanentemente presos, aguardando eternamente por uma liberação que nunca ocorrerá (ref pacheco p.132).

<!--TODO: perguntar se deadlocks só podem acontecer se houver acesso dentro de uma seção crítica a um recurso dentro de uma seção crítica (outra ou tem como ser a mesma?) -->

### Ferramentas Clássicas de Sincronização e Paralelização

Com todos os desafios da programação paralela e concorrente, são necessárias ferramentas e métodos para evitá-los e contorná-los. A seguir, são descritos os mais básicos.

A paralelização de algoritmos nem sempre é trivial. Além de certos trechos não serem paralelizáveis, durante a execução não há garantias acerca da ordem de execução dos passos entre threads, ou seja, não há garantias de que uma thread alcança um certo ponto do algoritmo antes da outra, comprometendo a integridade dos resultados. Serão abordados alguns dos problemas mais comuns de algortimos paralelos a seguir.

#### Mutexes, Semáforos e Wait

Para garantir que seções críticas sejam executadas por uma única thread a cada instante, devemos implementar a **exclusão mútua**, e o método mais comum de de fazê-lo é através de **mutexes** (mutual exclusion lock). Trata-se de um objeto ou variável adquirido por uma thread no início de uma seção crítica que permite que siga com suas tarefas enquanto todas as outras threads ficam paradas, **esperando** (**waiting**) no início da seção crítica até que a primeira thread devolva ou libere a mutex. Nesse instante, uma thread vai adquirir a mutex e seguir adiante e as outras continuarão esperando.

Em algumas circunstâncias, uma certa seção crítica pode ser acessada por um número limitado de threads (como no problema do produtor com muitos consumidores). Para esses casos, pode-se usar um **semáforo**, similar a uma mutex com um contador embutido. Sempre que uma thread começa a trabalhar na seção crítica utiliza-se o contador para notificar as outras threads e fazê-las aguardar ou seguir, de acordo com o limite estabelecido.

Vale notar que mutexes, wait e semáforos também se aplicam para processos concorrentes numa mesma thread que compartilhem recursos.

#### Join

Mesmo sem mutexes ou semáforos explícitos, o conceito de aguardar por outras threads ou processos ainda é relevante. Threads costumam ser invocadas (ou tecidas) a partir de uma thread pai, assim como processos concorrentes. Para aguardar pelo retorno de resultados ou término da execução de uma thread ou processo filho,

#### Alças de Threads (Thread Handles)

Linguagens modernas de programação abstraem o controle de threads usando objetos chamados **thread handles**, contendo as informações necessárias para identificar e interagir com threads. Em linguagens orientadas a objeto ou que incorporam elementos de orientação a objeto é uma abstração muito natural e as várias ferramentas como join são métodos. Em C, por outro lado, é necessário tratar de threads através dos seus identificadores de processo, etc, tornando a funcionalidade mais obtusa e esotérica para os "não iniciados".

### Modelos de Paralelismo

A diferença crucial entre as diversas implementações de paralelismo é o compartilhamento de recursos, afinal de contas, se nenhum recurso tem que ser compartilhado entre threads (como IO ou variáveis) não há como ocorrer condições de corrida ou deadlocks, restando somente o desafio de sincronização e a limitação da memória.

#### Memória Compartilhada

Via de regra, threads possuem seus próprios contextos (stacks, variáveis, heaps, etc).

cache tem um grande impacto em paralelismo que utiliza memória compartilhada (ref pacheco p.251)

#### Troca de Mensagens

O cerne da troca de mensagens (ou message-passing) é o par de operações envio-recebimento de valores entre threads em uma operação atômica, muito similar ao conceito produtor-consumidor.

Ao evitar que threads compartilhem memória e garantindo a transmissão atômica dos valores entre as mesmas, a consistência dos dados é garantida. Adicionalmente, se o recebimento das mensagens for uma operação bloqueante (ou seja, coloca a thread em espera até que haja um valor para ser consumido do outro lado), a chance de ocorrer condições de corrida é reduzida enormemente.

O modelo de troca de mensagens não vem de graça, contudo. É necessário que várias mudanças sejam feitas no algoritmo para comportar tal modelo.

#### Promessas e Objetos Futuros

Também conhecidos como futures, trata-se de uma poderosa abstração, na qual o conteúdo de uma variável ou objeto, resultado de alguma computação custosa, é delegado a uma nova thread ou processo enquanto o processo principal segue adiante. No instante em que o valor da variável ou objeto é necessário, a thread ou processo principal para e espera até que a computação do conteúdo seja concluída e o resultado seja armazenado na variável relevante (isso se já não tiver sido). A ideia central é a promessa de que, no futuro, quando a variável ou objeto for necessária, a computação estará concluída.

#### Threads Verdes vs Threads Verdadeiras

Invocar uma thread tipicamente é uma operação bastante custosa e certas linguagens optam por disponibilizar uma abstração aos desenvolvedores ao invés de threads de sistema. Estas são chamadas **green threads** ou threads virtuais. A criação e escalonamento de green threads são feitos em userspace, ao invés de kernelspace (TODO: REFERÊNCIA) e menos recursos são dedicados a cada thread, tornando-as leves, rápidas de criar e destruir. Green threads também podem ser criadas aos montes, em número muito maior que o número de núcleos disponíveis, permitindo comportamento similar a paralelo mesmo em ambientes sequenciais, mesmo se não houver

#### Threadpooling

Threadpooling consiste na criação de uma reserva (pool) de threads verdadeiras (OS Threads) uma única vez durante o código e a delegação de tarefas às mesmas, criando assim uma camada de abstração. Já que a criação e destruição de threads é bastante custoso, reutiliza-se as threads ao longo do algoritmo. Em contraponto, não há um controle tão fino e garantido de quantos "workers" estão trabalhando em uma dada tarefa a cada instante.

#### Corrotinas

Corrotinas são, em essência, rotinas interruptíveis, ou seja, sua execução pode ser interrompida e retomada posteriormente. A princípio, corrotinas são uma implementação direta do conceito de concorrência, em que se trocar o contexto por outra corrotina e depois voltar sem prejuízo para o resultado final.

Como comentado anteriormente, concorrência e paralelismo estão intimamente ligados, e pode-se extender o conceito de corrotinas para sistemas paralelos. Afinal de contas, os mesmos problemas que dificultam programação paralela também ocorrem em programas concorrentes: condições de corrida, deadlocks e a necessidade de sincronização e espera.

<!-- TODO: faz sentido dizer que problemas paralelos são um subset dos problemas concorrentes?? ou vice-versa?? -->

<!-- TODO: como deadlock pode ocorrer em programas concorrentes mas não paralelos? -->

## Linguagens e Paralelismo

<!-- TODO: faz sentido descrever aqui os programas usados? -->

O intuito central deste trabalho é estudar as abordagens de algumas linguagens de programação modernas quando se trata de paralelismo em eficiência, mas principalmente, ergonomia.

Nesse âmbito, entende-se por ergonomia a facilidade de aprender e utilizar as linguagens de programação e seus respectivos ecosisstemas, gerenciadores de pacote, etc, com um objetivo definido em mente. Uma linguagem mais ergonômica é aquela cujos conceitos e ferramentas são intuitivos, poderosos e fáceis de usar, poupando dores de cabeça ao programador. Assembly é um exemplo de linguagem pouco ergonômica. Enquanto C faz um melhor trabalho nesse aspecto, Python é ainda mais ergonômica para tarefas mais cotidianas, poupando o usuário do trabalho de gerenciar a memória explicitamente, apesar de ser menos eficiente. Linguagens de programação são ferramentas, afinal de contas, e mesmo utilizando duas ferramentas voltadas para o mesmo fim, uma pode ser mais confortável.

As quatro linguagens escolhidas foram: Python, por sua imensa difusão e facilidade de uso e aprendizado; Go, por sua popularidade, facilidade de aprendizado e por ter sido projetada com concorrência em mente; Rust, por ser uma linguagem de sistema poderosíssima e por seu modelo de gerenciamento de memória inovador; e Kotlin, por se propor a ser um sucessor de uma das mais difundidas linguagens de programação da atualidade (Java) e pelo suporte a corrotinas.


### Python

De acordo com a Developer Survey 2020 do StackOverflow (https://insights.stackoverflow.com/survey/2020 , acessado em 24/08/2021), Python é a terceira linguagem de programação mais amada e a décima com os maiores salários. Utilizada até pela NASA (https://www.python.org/about/success/usa/, acessado em 24/08/2021), Python se solidificou como uma linguagem padrão para todo tipo de aplicação que não demande respostas rápidas (como certos equipamentos médicos) com seu ecosistema rico, em especial aprendizado de máquina e data science.

#### Ambiente de Execução: Interpretador CPython

Python é uma linguagem de programação interpretada e seu interpretador padrão é o CPython, amplamente disponível. Pode ser facilmente obtido através dos repositórios padrão do Linux ou através do site, para Windows.

#### Paradigma: Orientação a Objeto/Multiparadigma

Multiparadigma, python é o pato das linguagens: voa, nada até faz café, mas não é especialista em nenhuma aplicação. Entretanto, o paradigma que se sobresai é a Orientação a Objeto.

#### Tipagem: Dinâmica

Python é uma linguagem com tipagem forte mas dinâmica, dotada de duck typing e inferência de tipos, e com coerções corriqueiras de tipos (mas não tão forçadas quanto Javascript). Essas características, em especial duck typing e tipagem dinâmica, são duas das maiores contribuições para a facilidade de adoção da linguagem.

#### Gerenciamento de Memória: Coleta de Lixo

Python possui coleta de lixo como modelo de gerenciamento de memória padrão (no interpretador CPython), forçando interrupções periódicas do algoritmo para desalocação de memória antiga e inútil, sacrificando desempenho por ergonomia.

#### GIL: Global Interpreter Lock <!--Problema-->

O interpretador padrão CPython possui uma trava global (GIL -- Global Interpreter Lock), que faz com que somente uma thread execute a cada instante, garantindo que não ocorram condições de corrida e escalonando as outras threads quando há operações de IO, costumeiramente demoradas (ref: Mark Lutz - Programming Python-O'Reilly Media (2006)). Trata-se de uma solução efetiva para os problemas de concorrência e paralelismo, mas pouco produtivo, já que código em python não pode ser verdadeiramente paralelo (Mark Lutz - Programming Python-O'Reilly Media (2006)).

#### ThreadPooling, ProcessPooling <!--Ferramenta usada-->

Foi utilizado um módulo que implementa threadpooling e processpooling. A diferença reside no fato que com processpooling as tarefas são despachadas para processos ao invés de threads. Há essa alternativa porque como Python possui o GIL, em certas circunstâncias é mais produtivo despachar as tarefas para novos processos; novas instâncias de interpretadores, cada um com sua GIL, funcionando em paralelo. A expectativa é que processpooling supere threadpooling, dado que serão usados algoritmos com praticamente nenhum IO.

#### Futures (Objetos Futuros)

Além de pooling, foram usados futures, uma implementação de objetos futuros.

#### Problemas e Desconfortos

O primeiro e mais óbvio dos desconfortos com o método de criação de threads ou despacho de tarefas para a reserva de threads ou processos é o fato que não é possível definir uma função in-line sem que seja uma equação lambda. Desse modo, é necessário criar funções auxiliares e enviá-las como parâmetro da função criadora ou expedidora (dispatcher). Além disso, como a função é um parâmetro, os parâmetros desta devem ser enviados como novos parâmetros. Veja:

```python3
def aux(param1, param2, param3)
    pass

for i in range(n_threads):
    thread.start_new(aux, (p1, p2, p3))
```

Há um grande desconforto quando se trata da passagem e definição de parâmtros mistos, isto é, anônimos e explícitos. Deve-se seguir uma ordem específica que nem sempre é a mais intuitiva.

Como citado anteriormente, a abordagem de utilizar uma trava global é bastante frustrante, do ponto de vista do desempenho. Fica claro que python não tem pretensão de ser uma linguagem capaz de competir pelo pódio de eficiência.

Como é de se esperar de uma linguagem interpretada com várias checagens em runtime, o pré-processador não é dos mais poderosos. Enquanto Go é capaz de prever certos deadlocks e Rust garante a segurança da memória, python permite que o programador siga em frente por sua conta e risco.

#### Vantagens e Ergonomia

Apesar das inconveniências, o ecossistema do Python é muito maduro e rico. o Pip, o gerenciador de pacotes, é excelente e fácil de se usar, diferente do que ocorre em Kotlin. Não foi utilizado nos experimentos desse trabalho, mas o gerenciamento de ambientes de execução de python, como virtualenv e anaconda são um tanto estranhos à primeira vista, mas são funcionais e muito úteis em projetos mais complexos.

Com o risco de algumas esquisitices ocasionais e erros de tipos, duck typing de python é uma mão na roda para qualquer programador, acelerando enormemente o desenvolvimento.

### Go

De acordo com a Devoloper Survey 2020 do StackOverflow (https://insights.stackoverflow.com/survey/2020 , acessada em 24/08/2021), Go é a quinta linguagem mais amada, subindo da décima posição no ano anterior. Com primitivas de paralelismo e concorrência em evidência, embutidas na linguagem, das linguagens estudadas Go é a mais fácil de botar a mão na massa.

#### Compilador <!-- TODO como eu escrevo isso direito? -->

Diferente de Python, Go é uma linguagem compilada com pretensão de ser veloz além de conveniente e fácil de aprender.

#### Paradigma: Estruturado e Concorrente

Go é uma linguagem imperativa e estruturada com vários elementos de orientação a objetos, como métodos, mas não herança.

#### Tipagem: Estática

Go possui tipagem forte e estática, dotada de alguma medida de duck typing e inferência de tipos. Diferente de Python, Go faz poucas coerções de tipo, inclusive não convertendo automaticamente inteiros para floats.

#### Gerenciamento de Memória: Coleta de Lixo

Go, apesar de compilada, possui um coletor de lixo que roda junto do processo principal. Apesar de ser paralelo, o coletor de lixo pausa a execução de todas as rotinas em execução por um instante para garantir a consistência dos dados (https://go.dev/blog/ismmkeynote, acessado em 24/08/2021)

#### Corrotina (Goroutines)

As goroutines, primitivas essenciais de concorrência em Go, são corrotinas em sua essência. Contudo, só é permitido que o runtime interrompa as corrotinas em certos pontos e não necessariamente são paralelas, mas são garantidamente recorrentes. Isso garante interrupções mais seguras.

#### Threads Verdes

Cada goroutine é similar a uma thread verde no sentido de que o mínimo de recursos é alocado para cada uma durante sua criação e execução, permitindo a criação de uma miríade de corrotinas (https://golang.org/doc/faq, acessado em 24/08/2021)

#### Canais e Comunicação Entre Threads

Em Go, compartilhamento de memória é fotemente desencorajado. É preferível utilizar, em seu lugar, a implementação de troca de mensagens: canais.

Canais devem ser criados em uma goroutine e compartilhados. A operação de ler de um canal bloqueia uma goroutine até que um valor seja enviado através dele, consumindo-o, então tem embutida função de sincronização. A escrita, contudo, não é uma operação bloqueante, e uma fila sem ordem garantida se forma quando há várias escritas no mesmo canal.

#### Problemas e Desconfortos

A instalação oficial da linguagem no linux não usa os gerenciadores de pacotes tradicionais, apesar de estar disponível via snapcraft e sdk. Seria bom se houvesse um esforço da própria Google para disponibilizar essas linguagens nos repositórios mais comuns.

Não é óbvio se isso é uma desvantagem, mas Go possui pouca coerção de tipos, o que força o programador a se atentar para coerência dos dados que está usando, mas deixa algumas linhas de código particularmente atrozes.

#### Vantagens e Ergonomia

Não foi necessário, mas Go tem um gerenciador de pacotes simples e efetivo, instalado juntamente com a linguagem em si.

Inicializar uma goroutine é trivial e está enraizado na linguagem e em seu propósito. Qualquer função pode ser invocado como corotina paralela só adicionando "go" antes, mesmo funções anônimas.

As regras de escopamento de Go permitem a definição de funções dentro do escopo de outras e também permite que sejam anônimas. Desse modo, torna-se muito conveniente e fácil definir um trecho de código in-line para ser executado como uma goroutine. Além disso, é fácil enviar cópias de variáveis para dentro do contexto dessas novas rotinas.

<!-- TODO: reescrever esse parágrafo aqui: -->
Não sei se é vantagem, mas memória compartilhada não funciona bem em Go. "Don't communicate by sharing memory; share memory by communicating."


### Rust

Com uma margem de quase 20 pontos percentuais em relação ao segundo lugar, Rust ficou no topo da categoria "linguagem mais amada". São cinco anos consecutivos na frente de linguagens como Python, Kotlin, Go, Typescript e Swift (https://insights.stackoverflow.com/survey/2020#most-loved-dreaded-and-wanted, acessado em 24/08/2021).

#### Compilador: rustc

Vigilante, intransigente, robusto e poderoso, o compilador de rust garante segurança e consistência, e desse modo pode fazer várias otimizações agressivas.

#### Paradigma: Estruturado++

Rust é uma linguagem de sistema que busca desempenho e ergonomia através de abstrações com custo zero, contando com seu compilador robusto para viabilizá-las. Rust incorpora vários elementos de orientação a objeto e programação funcional.

#### Gerenciamento de Memória: Escopamento, Ownership e Borrow Checker

Um dos maiores atrativos de Rust é seu inovador sistema de gerenciamento de memória. Através de empréstimos e checagens de dono (borrow e ownership) em tempo de compilação e tempo de vida baseado em escopos, Rust tira o peso de alocar e desalocar memória dos ombros do programador sem necessitar de coleta de lixo (e consequentemente sem runtime).

Por padrão, as variáveis em Rust são imutáveis, e quando mutáveis, só podem ser modificadas em escopos que possuam seu "ownership".

#### Tipagem: Estática

Kotlin é uma linguagem com tipagem forte e estática, mas com suporte a inferência de tipos.

#### Operações Atômicas

Não foi necessário, mas é possível envelopar um tipo qualquer em um Arc (Atomically Reference Counted), que garante que as operações efetuadas sobre uma de suas instâncias são atômicas. Desse modo é possível compartilhar memória com segurança e com poucas linhas de código a mais.

#### Funções in-line <!--Ferramenta usada-->

Closures em Rust são uma mão-na-roda, e encaixam perfeitamente com a expectativa dos construtores de threads de receberem uma função. Diferente de Kotlin que expera um bloco de código, mas mais conveniente que python, que espera uma função e os parâmetros como parâmetros diferentes do construtor.

#### Problemas e Desconfortos

Rust é uma linguagem difícil de se aprender. Seu modelo de gerenciamento de memória inovador pode ser muito frustrante e abstrato às vezes, apesar de não parecer esotérico como Haskell.

Rust, assim como Go, faz pouca coerção de tipos, o que garante coerência entre os tipos, importantíssimo em uma linguagem de sistemas.

Por rust ser uma linguagem de sistema, a sintaxe às vezes fica um pouco carregada e muita responsabilidade é colocada nas mãos do programador. Definitivamente não é uma linguagem para tarefas bobas, curtas e sujas, como python.

<!-- TODO: deixar esse parágrafo? rewrite? -->
É uma inconveniência pequena, mas a contagem de tempo de Rust é muito teimosa. Cisma em colocar a unidade de tempo no final e não consegui separar uma coisa da outra apropriadamente.

O maior dos desconfortos, de longe, é o compilador. Intransigente, lidar com o borrow checker é uma enorme dor de cabeça se você não tem experiência com a linguagem.

#### Vantagens e Ergonomia

A maior das vantagens de Rust é o compilador intransigente. No fim das contas é a peça que garante que a linguagem seja tão veloz e segura. É uma das principais características da linguagem, e com experiência, se torna uma ferramenta indispensável. Pode-se dizer que o modelo de gerenciamento de memória do Rust é um paradigma em si.

Ao incorporar vários elementos de orientação a objeto e programação funcional, como métodos, um sistema de tipos intrincado e closures, e compilar para código binário, Rust se torna uma alternativa confortável para C e C++.

o ambiente todo é muito bom e sensato. Rust é instalado através do pacote rustup, que inclui o compilador (rustc) e Cargo, o gerenciador de pacotes e aplicações. Desse modo, todo projeto em Rust tem uma organização semelhante. O próprio Cargo cuida de construir o projeto e executá-lo (cargo run, cargo build) e até produzir suas versões finais e otimizadas (cargo build --release, cargo run --release). É importante ressaltar que o cargo não é um gerenciador intrusivo ou excessivamente verborrágico, criando o mínimo de "infraestrutura" necessária (alguns poucos diretórios e alguns poucos arquivos, diferente de Gradle, que cria seis níveis de diretórios para um projeto simples).

Com Cargo, há um gerenciamento sensato de dependências e ambiente de execução: Cada projeto tem suas próprias crates (bibliotecas externas, instaladas através do arquivo com as dependências cargo.toml pelo Crate). Os pacotes ficam em um repositório no qual é fácil publicar suas próprias crates.

O serviço de otimização do compilador é poderosos e facilmente utilizado: basta adicionar a flag --release no comando cargo run. Tive que sacanear ele um pouco pra não pular todo o código que eu queria executar. Foi a única linguagem que fez algo assim.

Arcs, variáveis com operações atômicas, são facílimos de se implementar e poupam a dor de cabeça (e ameaça de deadlocks acidentais) causados por mutexes, além da verbosidade evitada.

### Kotlin

Surgido da necessidade de um substituto moderno para Java, especialmente para desenvolvimento mobile, Kotlin é a quarta linguagem mais amada na pesquisa Devoloper Survey 2020 do StackOverflow (https://insights.stackoverflow.com/survey/2020 , acessada em 24/08/2021), ficando atrás de Python, Typescript e Rust, e à frente de Go. De 2019 em diante o desenvolvimento Android é preferencialmente em Kotlin (https://kotlinlang.org/docs/android-overview.html, acessado em 24/08/2021).

#### Ambiente de Execução: Máquina Virtual Java (JVM)

A principal vantagem que Kotlin oferece é sua ubiquidade. Kotlin foi projetado para ser compilado para a JVM e, por consequência, funciona em uma miríade de dispositivos e plataformas diferentes, desde celulares a computadores pessoais.

Apesar de ter a JVM como ambiente de execução primário, o compilador de Kotlin, em tese, é capaz de compilar Kotlin para código nativo binário e para typescript, facilitando a integração da linguagem com aplicações web.

#### Paradigma: Orientado a Objetos

Kotlin, assim como Java, é uma linguagem orientada a objetos com alguns elementos de programação funcional tais quais funções-lambda e funções de ordem superior (como a maioria das linguagens modernas).

#### Gerenciamento de Memória: Coleta de Lixo (via JVM)

Kotlin utiliza o mesmo sistema de gerenciamento de memória de Java: o coletor de lixo da JVM.

#### Tipagem: Estática

Kotlin possui tipagem estática e forte, com inferência de tipos.

#### Corrotinas <!--Ferramenta usada-->

Foi utilizado um pacote que implementa corrotinas para Kotlin. Nele, corrotinas são marcadas com o descritor "suspend", que as torna suspendíveis, condição necessária para corrotinas. Além disso, corrotinas só podem ser chamadas de outras corrotinas, garantindo sincronização e escalonamento apropriado.

#### ThreadPooling (dispatchers) <!--Ferramenta usada-->

<!-- TODO: não sei como escrever isso aqui direito -->

#### Deferred (Objetos Futuros)

<!-- TODO: não sei como escrever isso aqui direito -->

#### Problemas e Desconfortos

Kotlin é desenvolvida majoritariamente pela JetBrains, apesar de ser um projeto Open Source. Devido a isso, há muita influência dos objetivos da empresa na linguagem e ecosistema. A criação de projetos, compilação e gerenciamento de pacotes é muito trabalhoso sem a IDE da JetBrains. É profundamente frustrante ver uma linguagem interessante e ambiciosa como Kotlin influenciada tão fortemente por interesses empresariais. Rust é melhor nesse aspecto, mesmo sendo amplamente financiada pela Mozilla.

A Documentação do Kotlin no site oficial deixa a desejar. Muitos dos exemplos partem do pressuposto que você estará usando a IDE IntelliJ, produto da JetBrains, e outras partes têm explicações incompletas ou sem exemplos de qualidade.

Como dito anteriormente, o gerenciador de projeto e dependências mais apropriado é o Gradle, utilizado em projetos Java. Diferente do Cargo, o Gradle cria uma quantidade relativamente grande de diretórios e arquivos em cada projeto. Por padrão, o código-fonte Kotlin fica soterrado sob seis níveis de diretórios. É compreensível que seja necessário para projetos complexos, especialmente de Java, contudo.

As mensagens de erros de Kotlin não são tão boas quanto as de outras linguagens como Rust.

#### Vantagens e Ergonomia

Kotlin possui uma sintaxe bem mais concisa e intuitiva que Java, sua comparação mais direta. A adoção da linguagem não é tão ágil quanto Go, mas mais simples do que Rust.

Kotlin pode ser compilado para a JVM, código binário nativo ou JS. Embora não tenha conseguido fazer o compilador fazer nada disso através da linha de comando.

O suporte à corrotinas é muito bom, embora não faça parte da biblioteca padrão (trata-se de uma biblioteca da JetBrains, citada e usada extensivamente na documentação mas só pode ser incluída no projeto usando a IDE ou Gradle). Transformar uma função em corrotina é muito fácil: basta adicionar o descritor "suspend"

O código concorrente pode ser fornecido através de um bloco de código, tornando a transição muito natural e intuitiva, similar a funções inline.

<!-- TODO: compilar uma tabela com atributos mais importantes das ling acima -->

## Experimentos e Resultados

A fim de comparar, em linhas gerais, a eficiência bruta das linguagens, mas muito mais importante, seus respectivos speedups, foram escolhidos dois problemas simples e trivialmente paralelizáveis: a computação do número pi através da série de Leibniz e a multiplicação de duas matrizes.

Justifica-se a utilização de problemas triviais com o fato de que os algoritmos em si não são o foco deste trabalho, mas sim os ganhos de desempenho e a ergonomia das linguagens. Desse modo, é irrelevante que um algoritmo intrincado e otimizado seja usado, e portanto, utilizou-se as abordagens mais ingênuas e diretas.

Decidiu-se por utilizar dois programas diferentes para investigar se haveria diferença significativa no speedup para problemas memory-bound e cpu-bound. Esperava-se que haveria uma diferença apreciável, afinal de contas, todas as threads têm que compartilhar o mesmo barramento de dados para acessar os valores na memória, e se parte significativa. Vale ressaltar que não é útil comparar os tempos de execução entre algoritmos, já que são vastamente diferentes, e a discrepância de velocidade entre linguagens é secundária.

### Descrição do Algoritmo CPU-Bound: Computação do Número Pi

Escolheu-se a computação do número pi através da série de leibniz por não utilizar mais de uma variável ao longo do laço de repetição e os cálculos a cada um serem custosos, relativamente à escrita: multiplicação, soma, e principalmente potência. Segue a fórmula:

\begin{equation}
    \sum_{n=0}^{\infty} \frac{\left ( -1 \right )^{n} }{ 2n+1 }
\end{equation}

Vale notar que a série converge muito lentamente, mas isso é irrelevante para o estudo, já que ocupar o processador é o foco.

### Descrição do Algoritmo Memory-Bound: Multiplicação de Matrizes

### Escolha das Linguagens

Definidos os dois problemas que seriam utilizados,

### Execução dos
Cada combinação de código e número de threads foi executado 30 vezes (totalizando 30x4x6 execuções) com auxílio de um script bash para mitigar os efeitos das variações aleatórias no desempenho, e os resultados foram armazenados em arquivos.




## Conclusão
Python tomou um pau. Mesmo sendo o mais direto de programar, não tenho muita segurança para projetos maiores ou mais arriscados
