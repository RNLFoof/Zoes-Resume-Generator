from pylatex import Document, Section, Itemize

from classes.SkillSet import SkillSet

if __name__ == '__main__':
    SkillSet._dump_schema()
    SkillSet.all()
    doc = Document('Resume')
    with doc.create(Section('Header')):
        doc.append('Zoe Zablotsky'.upper())
    with doc.create(Section('Skills')):
        with doc.create(Itemize()) as itemize:
            for skill in SkillSet.all().skills_by_generic_value():
                itemize.add_item(f"{skill.name} ({skill.generic_value()})")
                with doc.create(Itemize()) as subitemize:
                    subitemize.add_item(f"RELEVANT PROJECTS")
                    with doc.create(Itemize()) as subsubitemize:
                        subsubitemize.add_item(f"COOL PROJECT, in that CONNECTION")
                        subsubitemize.add_item(f"COOL PROJECT, in that CONNECTION")
                with doc.create(Itemize()) as subitemize:
                    subitemize.add_item(f"TRANSFERABLE SKILLS")
                    with doc.create(Itemize()) as subsubitemize:
                        subsubitemize.add_item(f"COOL PROJECT, in that CONNECTION")
                        subsubitemize.add_item(f"COOL PROJECT, in that CONNECTION")

    doc.generate_pdf(clean_tex=True)
