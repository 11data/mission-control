describe('Opportunities flows', () => {
  it('loads the Opportunities page', () => {
    cy.visit('/opportunities.html')
    cy.contains('Opportunities')
  })

  it('creates a new opportunity', () => {
    cy.visit('/opportunities.html')
    cy.get('#newOpp').click()
    cy.get('#title').type('Test Opportunity')
    cy.get('#company').type('ACME')
    cy.get('#value').type('10000')
    cy.get('#create').click()
    cy.contains('Test Opportunity')
  })

  it('drags an opportunity between stages', () => {
    // Manual or visual test: requires backend; placeholder for automation later
  })
})
