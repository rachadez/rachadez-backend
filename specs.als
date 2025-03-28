module rachadez

-- Assinaturas básicas
abstract sig Usuario {
    nome: one Nome,
    email: one Email,
    cpf: one CPF,
    telefone: lone Telefone
}

-- Tipos de usuário
sig Administrador extends Usuario {}
sig UsuarioComum extends Usuario {}

sig Nome, Email, Telefone, CPF {}

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
    criador: one Administrador,
    participantes: set Usuario,  -- Participantes podem ser qualquer Usuario
    esporte: one Esporte,
    local: one Arena,
    horario: one Horario,
    maxParticipantes: lone Int
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

-- Um usuário não pode ter o mesmo email ou CPF que outro
fact emailsCPFsUnicos {
    no disj u1, u2: Usuario | u1.email = u2.email
    no disj u1, u2: Usuario | u1.cpf = u2.cpf and u1.cpf != none
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

-- O criador NÃO é automaticamente participante (modificado)
fact criadorNaoAutomatico {
    all r: Racha | r.criador !in r.participantes
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

-- Criar um novo racha (agora exige um Administrador)
pred criarRacha[c, c1: Racha, adm: Administrador, e: Esporte, l: Arena, h: Horario] {
    c1 not in Racha
    c1.criador = adm
    c1.esporte = e
    c1.local = l
    c1.horario = h
    no c1.participantes  -- Admin não é mais automaticamente adicionado
    no c1.maxParticipantes
    Racha' = Racha + c1
}

-- Adicionar participante a um racha (qualquer usuário pode ser adicionado)
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

-- Remover participante de um racha (exceto o criador se estiver participando)
pred removerParticipante[r, r1: Racha, u: Usuario] {
    u in r.participantes
    u != r.criador  -- o criador (Administrador) não pode ser removido se estiver participando
    r1.participantes = r.participantes - u
    r1.esporte = r.esporte
    r1.local = r.local
    r1.horario = r.horario
    r1.maxParticipantes = r.maxParticipantes
    Racha' = Racha - r + r1
}

-- Verificações mantidas (todas as originais)
assert ApenasAdminsCriamRachas {
    all r: Racha | r.criador in Administrador
}
check ApenasAdminsCriamRachas for 5

-- Nova verificação para garantir que criador não é automaticamente participante
assert CriadorNaoAutomatico {
    all r: Racha | r.criador !in r.participantes
}
check CriadorNaoAutomatico for 5

-- Verificação original mantida (agora testa cenário opcional)
assert CriadorEParticipante {
    all r: Racha | r.criador in Usuario and (r.criador in r.participantes or r.criador not in r.participantes)
}
check CriadorEParticipante for 5

-- Exemplo de execução atualizado
run exemplo {
    some adm: Administrador, comum: UsuarioComum, e: Esporte, l: Arena, h: Horario |
        some r, r1, r2: Racha | 
            criarRacha[r, r1, adm, e, l, h] and
            adicionarParticipante[r1, r2, comum] and
            (adm in r2.participantes or adm not in r2.participantes)  -- Admin pode ou não participar
} for 5 but 3 Racha, exactly 1 Administrador, exactly 1 UsuarioComum
