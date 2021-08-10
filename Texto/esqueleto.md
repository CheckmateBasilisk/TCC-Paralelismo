# TCC

## Introdução

- descrever a premissa e motivação
- descrever o que foi feito
- descrever brevemente os resultados
- tldr da conclusão

## Contextualização Teórica
intro
### Motivação: Limites Físicos da Lei de Moore
Lei de moore: a cada 2 anos aproximadamente o número de transistores dobra.

transistores vêm se tornando cada vez menores:
- microeletrônica complexa
- resfriamento impossível
- tunelamento de elétrons: destruição de dados

tornar hardware menor e mais poderoso está se tornando praticamente impossível. Solução: refinar o software para funcionar em diversos hardwares simultâneamente.

### Paralelismo e Concorrência

Paralelismo: rodar ao mesmo tempo, em vários workers diferentes.
Concorrência: rodar junto, alternando atenção do worker.

paralelismo: cozinhar um almoço. Vários pratos fazendo progresso juntos.

paralelismo necessariamente é concorrente, a nível de sistema. A nível de worker talvez não, mas não parece uma má ideia.

### Problemas Comuns de Algoritmos Paralelos
problemas surgem do fato que não há garantia de ordem de execução do código entre as threads. Não dá para garantir que uma das threads vai acessar antes do que a outra ou vice-versa.

#### Corrida

Duas threads diferentes acessando (ou tentando acessar) a mesma região da memória. Como não há garantia de em que momento o scheduler interromperá a execução de uma thread para dar sequência a outra tarefa na mesma thread, é possível que o acesso seja feito sobre valores desatualizados (ou até corrompidos) e as operações subsequentes não sejam mais relevantes.

#### Sincronização

Às vezes uma thread deve

#### Atomicidade de Operações Críticas
#### Deadlocks

### Ferramentas Clássicas de Sincronização e Paralelização
#### Conceito de Thread
#### Mutexes e Semáforos
#### Join e Wait
#### Alças de Threads (Thread Handles)

### Modelos de Paralelismo
#### Memória Compartilhada
#### Troca de Mensagens
#### Promessas e Objetos Futuros
kotlin: Deferred
python: futures
#### Threads Verdes vs Threads Verdadeiras
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
#### ?? <!--Problema-->
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
#### ?? <!--Problema-->
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
