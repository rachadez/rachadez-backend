module rachadez

abstract sig Bool{}
one sig True, False extends Bool {}

sig RachaDez {
	arenas: set Arena,
	usuarios: set Usuario,
	reservas: set Reserva
}

sig Arena {
	nome: String,
	descricao: String,
	capacidade: Int,
	tipo: String
}

sig Reserva {
	mat_aluno_responsavel: String,
	arena: one Arena,
}

sig Usuario {
	email: String,
	cpf: String,
	nome: String,
	senha: String,
	telefone: String,
	isBlocked: Bool,
	isAdmin: Bool,
}

sig UsuarioExterno extends Usuario {}

sig UsuarioInterno extends Usuario {}

sig Administrador extends Usuario {}

/* Fatos sobre usuários*/

fact "tiposUsuarios" {
	Usuario = UsuarioInterno + UsuarioExterno
}

/* Fatos sobre reservas */
pred adicionaReserva[s: RachaDez, r: Reserva] {
	r in s.reservas
}

pred adicionaReservaTeste[d,s: RachaDez, r: Reserva] {
	s.reservas = d.reservas + r
} 


/* 
pred adicionaArena[s: Sistema, a: Arena] {
	a in s.arenas
}
*/

run adicionaReservaTeste for 3 but 1 RachaDez, 2 Reserva

