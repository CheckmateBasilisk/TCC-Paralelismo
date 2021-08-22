# TCC

## Introdução

- descrever a premissa e motivação
- descrever o que foi feito
- descrever brevemente os resultados
- tldr da conclusão

## Contextualização Teórica

Neste capítulo serão abordados termos e conceitos centrais ao tema tratado: a diferença entre Paralelismo e Concorrência (seção xx), alguns problemas comuns que atormentam programadores que enfrentam algoritmos paralelos (seção xx), algumas ferramentas clássicas utilizadas para sincronizar e paralelizar algoritmos (seção xx), alguns dos modelos de paralelismo (seção xx) em especial os utilizaos pelas linguagens estudadas: Python, Go, Kotlin e Rust.

### Motivação: Limites Físicos da Lei de Moore

É inegável a importância da computação para a civilização humana moderna. É sabido também que a demanda por poder computacional vem crescendo vertiginosamente (em inúmeras áreas, desde a academia ao entretenimento) e até recentemente a microeletrônica foi capaz de acompanhar, reduzindo o tamanho dos componentes (em especial transistores) e produzindo chips cada vez mais complexos e poderosos. As maiores maravilhas da ciência dos últimos séculos cabem em uma miúda caixa de aço e silício em nossos bolsos, mas a tendência de incrementar mais e mais os processadores e chips está chegando em seu limite.

A Lei de Moore, postulada por Gordon E. Moore em 1965 (TODO: CITAÇÃO), afirma que a cada dois anos a densidade de transistores dobraria, fazendo crescer consigo a potência dos dispositivos. Não é surpresa que eventualmente um limite superior seria atingido sem uma mudança radical de paradigma. Dentre as razões estão: a imensa complexidade da microeletrônica envolvida, a impossibilidade de se resfriar os componentes e, surpreendentemente, o tunelamento dos elétrons entre os componentes, destruindo os dados.

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
<!--
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

<!-- colocar fórmula da lei de amdahl -->

Percebe-se que quando o número de threads tende ao infinito, o tempo total de execução do algoritmo tende à soma das seções sequenciais. Na prática o custo combinado do gerenciamento das threads cresce, produzindo um ponto de mínimo no qual o ganho é máximo em comparação ao incremento.

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

Linguagens modernas de programação abstraem o controle de threads usando objetos chamados **thread handles**, contendo as informações necessárias para identificar e interagir com threads. Em linguagens orientadas a objeto ou que incorporam elementos de orientação a objeto (como as estudadas) é uma abstração muito natural e as várias ferramentas como join são métodos. Em C, por outro lado, é necessário tratar de threads através dos seus identificadores de processo, etc, tornando a funcionalidade mais obtusa e esotérica para os "não iniciados".

### Modelos de Paralelismo
#### Memória Compartilhada



cache tem um grande impacto em paralelismo que utiliza memória compartilhada (ref pacheco p.251)

#### Troca de Mensagens
#### Promessas e Objetos Futuros
kotlin: Deferred
python: futures
#### Threads Verdes vs Threads Verdadeiras

Invocar uma thread tipicamente é uma operação bastante custosa e certas linguagens optam por disponibilizar uma abstração aos desenvolvedores ao invés de threads de sistema. Estas, são chamadas **green threads** ou threads virtuais. A criação e escalonamento de green threads são feitos em userspace, ao invés de kernelspace (TODO: REFERÊNCIA) e menos recursos são dedicados a cada thread, tornando-as leves, rápidas de criar e destruir, mas menos potentes por não serem threads nativas.

#### ThreadPooling
python: threadpool/processpool
#### Corrotinas
Corrotina é concorrência, a princípio. Fácil (conceitualmente, mas não na prática, provavelmente) de extender para paralelismo, se adicionar uns constraints extras.


## Linguagens e Paralelismo
### Python
#### Paradigma: Orientação a Objeto/Multiparadigma
#### Gerenciamento de Memória: Coleta de Lixo
#### Ambiente de Execução: Interpretador CPython
#### Tipagem: Dinâmica
#### GIL: Global Interpreter Lock <!--Problema-->
#### ThreadPooling, ProcessPooling <!--Ferramenta usada-->
#### Futures <!--Ferramenta usada-->
#### Problemas e Desconfortos
é necessário enviar uma função para o criador de threads. Python não tem um mecanismo fácil de criar funções inline.
A abordagem do GIL é muito... estranha. Permitir paralelismo impedindo paralelismo não parece fazer sentido. Contudo, permite concorrência.
Python é interpretado. Diferente de Rust, não há checagens muito poderosas antes do runtime.
#### Vantagens e Ergonomia
Ecosistema muito maduro. Gerenciador de pacotes bom. Gerenciamento de ambiente de execução é meio estranho, mas funcional.
duck-typing facilita a vida e acelera desenvolvimento (com risco de algumas esquisitices)

### Go
#### Paradigma: Estruturado e Concorrente
#### Gerenciamento de Memória: Coleta de Lixo
#### Compilador / Ambiente de Execução: SO <!-- TODO como eu escrevo isso direito? -->
#### Tipagem: Estática
#### Corrotina (Go Routines) <!--Ferramenta usada, vale a pena comentar já? ou melhor deixar pra Kotlin aprofundar? Talvez trocar a ordem...-->
Go Routines são, no fim das contas, corrotinas necessariamente paralelas. Kotlin é mais puro nisso.
#### Threads Verdes <!--Ferramenta usada-->
Goroutines são Threads Verdes
#### Canais e Comunicação Entre Threads <!--Ferramenta usada-->
ler de um canal é uma operação bloqueante! (serve como sincronização (wait))
escrever em canal não é, então a ordem de escrita não é garantida.
#### Funções in-line <!--Ferramenta usada-->
escrever trechos de código
#### Problemas e Desconfortos
a instalação da linguagem no linux não usa gerenciador de pacotes.
Go pouca coerção de tipos. Pode ser bom, mas algumas linhas podem ficar atrozes de se ler.
#### Vantagens e Ergonomia
não foi necessário, mas Go tem um gerenciador de pacotes (go get <package>)
inicializar uma goroutine é trivial e está enraizado na linguagem e em seu propósito. Qualquer função pode ser invocado como corotina paralela só adicionando "go" antes
função inline é infinitamente útil e facilita o envio de cópias de variáveis para dentro de seu contexto.

### Rust
#### Paradigma: Estruturado++
Rust é uma linguagem de sistema
#### Gerenciamento de Memória: Escopamento, Ownership e Borrow Checker
imutabilidade por padrão
Ownership e Borrowing. Somente um
#### Compilador: rustc
Compilador brutal. Vigilante e intransigente, garante muuuuita coisa. Rust não tem runtime nenhum e o binário produzido consegue correr muito, por consequência.
#### Tipagem: Estática
#### Operações Atômicas <!--Ferramenta usada-->
Não foi necessário, ma sé possível envelopar um tipo qualquer em um Arc (Atomically Reference Counted), que garante que todas as operações efetuadas sobre uma de suas instâncias são atômicas.
#### Funções in-line <!--Ferramenta usada-->
Closures em Rust são uma mão-na-roda, e encaixam perfeitamente com a expectativa dos construtores de threads de receberem uma função. Diferente de Kotlin que expera um bloco de código, mas melhor que python, que espera uma chamada de função mesmo.
#### Problemas e Desconfortos
Rust é uma linguagem difícil de se aprender. Seu modelo de gerenciamento de memória inovador pode ser muito frustrante e abstrato às vezes (mas não chega a ser taumatúrgico como em Haskell).
Rust, assim como Go, faz pouca coerção de tipos. Pode ser bom, mas algumas linhas podem ficar atrozes de se ler.
Não é muito significativo, mas a contagem de tempo de Rust é muito teimosa. Cisma em colocar a unidade de tempo no final e não consegui separar uma coisa da outra apropriadamente.
Por rust ser uma linguagem de sistema, a sintaxe às vezes fica um pouco carregada e muita responsabilidade é colocada nas mãos do programador. Definitivamente não é uma linguagem para tarefas bobas, curtas e sujas, como python.
O compilador muito intransigente. Lidar com o borrow checker é uma dor de cabeça colossal se você não tem experiência com a linguagem (meu caso)
#### Vantagens e Ergonomia
O compilador é muito intransigente. Garante MUITA segurança. É uma das principais características da linguagem, afinal, e com experiência, se torna uma ferramenta indispensável. Pode-se dizer que o modelo de gerenciamento de memória do Rust é um paradigma em si.
o ambiente todo é muito bom e sensato. Rust vem através do pacote rustup, que inclui o compilador (rustc) e Cargo, o gerenciador de pacotes e aplicações. Desse modo, todo projeto em Rust tem a mesma cara e isso está acessível. O próprio Cargo cuida de construir o projeto e executá-lo (cargo run, cargo build) e até produzir suas versões finais e otimizadas (cargo build --release, cargo run release).
Gerenciamento sensato de dependências e ambiente de execução: Cada projeto tem suas próprias crates (bibliotecas externas, instaladas através do arquivo com as dependências cargo.toml pelo Crate). Isso garante a conteinerização dos projetos.
O serviço de otimização do compilador é assustador e facilmente utilizado (flag --release em cargo run). Tive que sacanear ele um pouco pra não pular todo o código que eu queria executar. Foi a única linguagem que fez algo assim.
Error Handling permeia Rust. Para esse projeto eu ignorei, mas é uma ferramenta muito útil e poderosa, especialmente quando combinada com o borrow checker e afins.
Apesar de ser uma linguagem de sistema estruturada, há muito de orientação a objeto incorporado em Rust, incrementando enormemente a ergonomia da linguagem. Desde coisas simples como métodos até estruturas similares a heranças e sobrecarga de métodos (exemplo: método print, usado na macro println!() ).


### Kotlin
#### Paradigma: Orientado a Objetos
#### Gerenciamento de Memória: Coleta de Lixo (via JRE)
#### Ambiente de Execução: Máquina Virtual Java (JRE)
#### Tipagem: Estática
#### ThreadPooling (dispatchers) <!--Ferramenta usada-->
#### Corrotinas <!--Ferramenta usada-->
#### Problemas e Desconfortos
Kotlin é cachorrinho da JetBrains, a empresa que faz e vende a IDE IntelliJ. O fluxo de criar projetos, compilá-los etc é uma dor de cabeça enorme sem ela. O gerenciamento de pacotes e ambiente é possível só através do Gradle ou Maven ou usando a IDE. É profundamente frustrante. Rust parece melhor que Kotlin nesse aspecto, além de não ficar escravo de uma corporação (mesmo que seja amplamente financiada pela Mozilla).
A Documentação do Kotlin no site oficial deixa a desejar. Muitos dos exemplos partem do pressuposto que você estará usando a IntelliJ e outras partes têm explicações incompletas ou sem exemplos decentes.
#### Vantagens e Ergonomia
Kotlin possui uma sintaxe bem mais concisa que Java; uma comparação justa de se fazer já que tem como objetivo substituir Java.
Kotlin pode ser compilado para a JVM, código binário nativo ou JS. Embora não tenha conseguido fazer o compilador fazer nada disso através da linha de comando.
O suporte à corrotinas é muito bom, embora não faça parte da biblioteca padrão (trata-se de uma biblioteca da JetBrains, citada e usada extensivamente na documentação mas só pode ser incluída no projeto usando a IDE ou Gradle). O código concorrente é dado através de um bloco de código, tornando a transição muito natural e intuitiva.

<!-- TODO: compilar uma tabela com atributos mais importantes das ling acima -->

## Experimentos e Resultados

## Conclusão
