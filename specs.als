module rachadez

-- Assinaturas básicas
abstract sig Usuario {
    nome: one Nome,
    email: one Email,
    telefone: lone Telefone
}

sig Nome, Email, Telefone {}

sig Arena {
    nome: one NomeArena,
    endereco: one Endereco,
    capacidade: lone Int
}

sig NomeArena, Endereco {}

sig Esporte {
    nome: one NomeEsporte
}

sig NomeEsporte {}

sig Racha {
    criador: one Usuario,
    participantes: set Usuario,
    esporte: one Esporte,
    local: one Arena,
    horario: one Horario,
    maxParticipantes: lone Int,
}

sig Horario {
    inicio: one Tempo,
    fim: one Tempo
}

sig Tempo {
    dia: one Int,
    hora: one Int,
    minuto: one Int
}

-- Fatos (restrições)

-- Um usuário não pode ter o mesmo email ou telefone que outro
fact emailsTelefonesUnicos {
    no disj u1, u2: Usuario | u1.email = u2.email
    no disj u1, u2: Usuario | u1.telefone = u2.telefone and u1.telefone != none
}

-- O horário de fim deve ser após o horário de início
fact horarioValido {
    all h: Horario | lt[h.inicio, h.fim]
}

-- Um usuário não pode participar de dois rachas no mesmo horário
fact semConflitoParticipacao {
    no disj r1, r2: Racha | 
        some u: Usuario | 
            u in r1.participantes and u in r2.participantes and
            conflitoHorario[r1.horario, r2.horario]
}

-- O criador de um racha é automaticamente participante
fact criadorEParticipante {
    all r: Racha | r.criador in r.participantes
}

-- O número de participantes não pode exceder o máximo (se definido)
fact limiteParticipantes {
    all r: Racha | some r.maxParticipantes implies #r.participantes <= r.maxParticipantes
}

-- Predicados e funções auxiliares
pred conflitoHorario[h1, h2: Horario] {
    not (lt[h1.fim, h2.inicio] or lt[h2.fim, h1.inicio])
}

pred lt[t1, t2: Tempo] {
    t1.dia = t2.dia and t1.hora = t2.hora implies t1.minuto < t2.minuto
    t1.dia = t2.dia implies t1.hora < t2.hora
    t1.dia < t2.dia
}

-- Operações (comandos)

-- Criar um novo racha
pred criarRacha[c, c1: Racha, u: Usuario, e: Esporte, l: Arena, h: Horario] {
    c1 not in Racha
    c1.criador = u
    c1.esporte = e
    c1.local = l
    c1.horario = h
    c1.participantes = u
    no c1.maxParticipantes
    Racha' = Racha + c1
}

-- Adicionar participante a um racha
pred adicionarParticipante[r, r1: Racha, u: Usuario] {
    u not in r.participantes
    some r.maxParticipantes implies #r.participantes < r.maxParticipantes
    r1.participantes = r.participantes + u
    r1.esporte = r.esporte
    r1.local = r.local
    r1.horario = r.horario
    r1.maxParticipantes = r.maxParticipantes
    Racha' = Racha - r + r1
}

-- Remover participante de um racha
pred removerParticipante[r, r1: Racha, u: Usuario] {
    u in r.participantes
    u != r.criador  -- o criador não pode ser removido
    r1.participantes = r.participantes - u
    r1.esporte = r.esporte
    r1.local = r.local
    r1.horario = r.horario
    r1.maxParticipantes = r.maxParticipantes
    Racha' = Racha - r + r1
}

-- Exemplo de verificação
assert CriadorEParticipante {
    all r: Racha | r.criador in r.participantes
}
check CriadorEParticipante for 5

-- Exemplo de execução
run exemplo {
    some u: Usuario, e: Esporte, l: Arena, h: Horario |
        some r, r1: Racha | criarRacha[r, r1, u, e, l, h]
} for 5 but 2 Racha
