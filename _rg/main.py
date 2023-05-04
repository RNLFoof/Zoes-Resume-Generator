from _rg.classes.PotentialContent import PotentialContent
from _rg.classes.RenderSettings import RenderSettings
from _rg.classes.Resume import Resume

if __name__ == '__main__':
    PotentialContent.dump_all_schemas()

    Resume().generate_pdf("out", RenderSettings())
    exit()

    doc = Document('Resume')
    with doc.create(Section('Heading')):
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
