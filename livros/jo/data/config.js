/**
 * Configuração do Livro de Jó
 * Este arquivo contém todos os dados estruturados do livro para uso nos elementos interativos.
 */

const BOOK_CONFIG = {
    // Metadados do livro
    meta: {
        name: 'Jó',
        abbrev: 'JO',
        testament: 'AT',
        category: 'poeticos',
        chapters: 42,
        verses: 1070,
        bibleUrl: 'https://www.bibliaonline.com.br/naa/jó'
    },

    // Personagens principais
    characters: [
        {
            id: 'jo',
            name: 'Jó',
            color: '#60a5fa',
            role: 'Protagonista',
            image: '../imagens/JO.png',
            description: 'Um homem íntegro e reto que temia a Deus. Perdeu tudo, mas manteve sua fé.',
            chapters: 23
        },
        {
            id: 'elifaz',
            name: 'Elifaz',
            color: '#fb923c',
            role: 'Amigo (Temanita)',
            image: '../imagens/ELIFAZ.png',
            description: 'O primeiro dos três amigos. Argumenta com base na experiência e tradição.',
            chapters: 4
        },
        {
            id: 'bildade',
            name: 'Bildade',
            color: '#a78bfa',
            role: 'Amigo (Suíta)',
            image: '../imagens/BILDADE.png',
            description: 'O segundo amigo. Apela à sabedoria dos antigos e à justiça retributiva.',
            chapters: 3
        },
        {
            id: 'zofar',
            name: 'Zofar',
            color: '#fb7185',
            role: 'Amigo (Naamatita)',
            image: '../imagens/ZOFAR.png',
            description: 'O terceiro amigo. O mais duro e dogmático em suas acusações.',
            chapters: 2
        },
        {
            id: 'eliu',
            name: 'Eliú',
            color: '#22d3ee',
            role: 'Jovem Sábio',
            image: '../imagens/ELIU.png',
            description: 'Filho de Baraquel. Intervém após os três amigos, propondo que o sofrimento é disciplina.',
            chapters: 6
        },
        {
            id: 'deus',
            name: 'Deus',
            color: '#34d399',
            role: 'O Todo-Poderoso',
            image: '../imagens/DEUS.png',
            description: 'Fala a Jó do meio de um redemoinho, revelando Sua soberania sobre a criação.',
            chapters: 5
        },
        {
            id: 'satanas',
            name: 'Satanás',
            color: '#ef4444',
            role: 'O Acusador',
            image: '../imagens/SATANAS.png',
            description: 'Desafia a integridade de Jó diante de Deus no tribunal celestial.',
            chapters: 2
        },
        {
            id: 'narrador',
            name: 'Narrador',
            color: '#d4a853',
            role: 'Prólogo/Epílogo',
            description: 'Voz narrativa que apresenta o contexto e conclusão da história.',
            chapters: 3
        }
    ],

    // Estrutura do livro
    structure: [
        { section: 'Prólogo', chapters: '1-2', type: 'prosa' },
        { section: 'Lamento de Jó', chapters: '3', type: 'poesia' },
        { section: 'Primeiro Ciclo de Debates', chapters: '4-14', type: 'poesia' },
        { section: 'Segundo Ciclo de Debates', chapters: '15-21', type: 'poesia' },
        { section: 'Terceiro Ciclo de Debates', chapters: '22-31', type: 'poesia' },
        { section: 'Discursos de Eliú', chapters: '32-37', type: 'poesia' },
        { section: 'Discursos de Deus', chapters: '38-41', type: 'poesia' },
        { section: 'Epílogo', chapters: '42', type: 'prosa' }
    ],

    // Temas principais
    themes: [
        { name: 'Sofrimento do Inocente', description: 'Por que os justos sofrem?' },
        { name: 'Teodiceia', description: 'Justiça de Deus diante do mal' },
        { name: 'Fé na Adversidade', description: 'Confiança mesmo sem entender' },
        { name: 'Limitação Humana', description: 'A incapacidade de compreender os caminhos de Deus' },
        { name: 'Redenção', description: 'O Redentor que vive (Jó 19:25)' }
    ]
};

// Exportar para uso em módulos ES6 ou acesso global
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BOOK_CONFIG;
}
