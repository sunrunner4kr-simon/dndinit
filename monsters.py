from database import db
import json

class Action():
  def __init__(self, attack_bonus, damage_dice, desc, name):
    self.attack_bonus = attack_bonus
    self.damage_dice = damage_dice
    self.desc = desc
    self.name = name 
  
class Reaction():
  def __init__(self, desc, name):
    self.desc = desc
    self.name = name 

class LegendaryAction():
  def __init__(self, desc, name):
    self.desc = desc
    self.name = name

class SpecialAbility():
  def __init__(self, desc, name):
    self.desc = desc
    self.name = name

class Monster(db.Model):

  slug = db.Column(db.String(30), primary_key=True)
  name = db.Column(db.String(30), unique=False, nullable=True)
  size = db.Column(db.String(10), unique=False, nullable=True)
  type = db.Column(db.String(20), unique=False, nullable=True)
  subtype = db.Column(db.String(20), unique=False, nullable=True)
  group = db.Column(db.String(20), unique=False, nullable=True)
  alignment = db.Column(db.String(20), unique=False, nullable=True)
  armor_class = db.Column(db.Integer, unique=False, nullable=False)
  armor_desc = db.Column(db.String(20), unique=False, nullable=True)
  hit_points = db.Column(db.Integer, unique=False, nullable=True)
  hit_dice = db.Column(db.String(20), unique=False, nullable=True)
  speed = db.Column(db.String(40), unique=False, nullable=True)
  strength = db.Column(db.Integer, unique=False, nullable=True)
  dexterity = db.Column(db.Integer, unique=False, nullable=True)
  constitution = db.Column(db.Integer, unique=False, nullable=True)
  intelligence = db.Column(db.Integer, unique=False, nullable=True)
  wisdom = db.Column(db.Integer, unique=False, nullable=True)
  charisma = db.Column(db.Integer, unique=False, nullable=True)
  strength_save = db.Column(db.Integer, unique=False, nullable=True)
  dexterity_save = db.Column(db.Integer, unique=False, nullable=True)
  constitution_save = db.Column(db.Integer, unique=False, nullable=True)
  intelligence_save = db.Column(db.Integer, unique=False, nullable=True)
  wisdom_save = db.Column(db.Integer, unique=False, nullable=True)
  charisma_save = db.Column(db.Integer, unique=False, nullable=True)
  perception = db.Column(db.Integer, unique=False, nullable=True)
  skills = db.Column(db.String(40), unique=False, nullable=True)
  damage_vulnerabilities = db.Column(db.String(40), unique=False, nullable=True)
  damage_resistances = db.Column(db.String(40), unique=False, nullable=True)
  damage_immunities = db.Column(db.String(40), unique=False, nullable=True)
  condition_immunities = db.Column(db.String(40), unique=False, nullable=True)
  senses = db.Column(db.String(40), unique=False, nullable=True)
  languages = db.Column(db.String(40), unique=False, nullable=True)
  challenge_rating = db.Column(db.String(10), unique=False, nullable=True)
  actions = db.Column(db.String(40), unique=False, nullable=True)
  reactions = db.Column(db.String(40), unique=False, nullable=True)
  legendary_desc = db.Column(db.String(40), unique=False, nullable=True)
  legendary_actions = db.Column(db.String(40), unique=False, nullable=True)
  special_abilities = db.Column(db.String(40), unique=False, nullable=True)
  spell_list = db.Column(db.String(40), unique=False, nullable=True)
  img_main = db.Column(db.String(40), unique=False, nullable=True)
  document__slug = db.Column(db.String(20), unique=False, nullable=True)
  document__title = db.Column(db.String(20), unique=False, nullable=True)
  document__license_url = db.Column(db.String(20), unique=False, nullable=True)

  def __init__(self,
                 slug: str,
                 name: str,
                 size: str,
                 type: str,
                 subtype: str,
                 group: str,
                 alignment: str,
                 armor_class: int,
                 armor_desc: str,
                 hit_points: int,
                 hit_dice: str,
                 speed: str,
                 strength: int,
                 dexterity: int,
                 constitution: int,
                 intelligence: int,
                 wisdom: int,
                 charisma: int,
                 strength_save: int,
                 dexterity_save: int,
                 constitution_save: int,
                 intelligence_save: int,
                 wisdom_save: int,
                 charisma_save: int,
                 perception: int,
                 skills: str,
                 damage_vulnerabilities: str,
                 damage_resistances: str,
                 damage_immunities: str,
                 condition_immunities: str,
                 senses: str,
                 languages: str,
                 challenge_rating: str,
                 actions,
                 reactions,
                 legendary_desc: str,
                 legendary_actions,
                 special_abilities,
                 spell_list: str,
                 img_main: str,
                 document__slug: str,
                 document__title: str,
                 document__license_url: str,

                 ):
        self.slug = slug
        self.name = name
        self.size = size
        self.type = type
        self.subtype = subtype
        self.group = group
        self.alignment = alignment
        self.armor_class = armor_class
        self.armor_desc = armor_desc
        self.hit_points = hit_points
        self.hit_dice = hit_dice
        self.speed = speed
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.strength_save = strength_save
        self.dexterity_save = dexterity_save
        self.constitution_save = constitution_save
        self.intelligence_save = intelligence_save
        self.wisdom_save = wisdom_save
        self.charisma_save = charisma_save
        self.perception = perception
        self.skills = skills
        self.damage_vulnerabilities = damage_vulnerabilities
        self.damage_resistances = damage_resistances
        self.damage_immunities = damage_immunities
        self.condition_immunities = condition_immunities
        self.senses = senses
        self.languages = languages
        self.challenge_rating = challenge_rating
        self.actions = actions
        self.reactions = reactions
        self.legendary_desc = legendary_desc
        self.legendary_actions = legendary_actions
        self.special_abilities = special_abilities
        self.spell_list = spell_list
        self.img_main = img_main
        self.document__slug = document__slug
        self.document__title = document__title
        self.document__license_url = document__license_url

  def to_dict(self):
    return {
      'slug': self.slug,
      'name': self.name,
      'size': self.size,
      'type': self.type,
      'subtype': self.subtype,
      'group': self.group,
      'alignment': self.alignment,
      'armor_class': self.armor_class,
      'armor_desc': self.armor_desc,
      'hit_points': self.hit_points,
      'hit_dice': self.hit_dice,
      'speed': self.speed,
      'strength': self.strength,
      'dexterity': self.dexterity,
      'constitution': self.constitution,
      'intelligence': self.intelligence,
      'wisdom': self.wisdom,
      'charisma': self.charisma,
      'strength_save': self.strength_save,
      'dexterity_save': self.dexterity_save,
      'constitution_save': self.constitution_save,
      'intelligence_save': self.intelligence_save,
      'wisdom_save': self.wisdom_save,
      'charisma_save': self.charisma_save,
      'perception': self.perception,
      'skills': self.skills,
      'damage_vulnerabilities': self.damage_vulnerabilities,
      'damage_resistances': self.damage_resistances,
      'damage_immunities': self.damage_immunities,
      'condition_immunities': self.condition_immunities,
      'senses': self.senses,
      'languages': self.languages,
      'challenge_rating': self.challenge_rating,
      'actions': self.actions,
      'reactions': self.reactions,
      'legendary_desc': self.legendary_desc,
      'legendary_actions': self.legendary_actions,
      'special_abilities': self.special_abilities,
      'spell_list': self.spell_list,
      'img_main': self.img_main,
      'document__slug': self.document__slug,
      'document__title': self.document__title,
      'document__license_url': self.document__license_url
    }

  def addMonsters(data):
        monster_entries = []
        for monster in data['results']:
          action_entries = []
          for action in monster['actions']:
            if 'attack_bonus' in action:
              newAction = Action( attack_bonus = action['attack_bonus'],
                                damage_dice = action['damage_dice'],
                                desc = action['desc'],
                                name = action['name'] )
            else:
              newAction = Action( attack_bonus = "",
                              damage_dice = "",
                              desc = action['desc'],
                              name = action['name'] )
            
            action_entries.append(newAction)
          reaction_entries = []
          for reaction in monster['reactions']:
            newReaction = Reaction( desc = reaction['desc'],
                                    name = reaction['name'] )
            reaction_entries.append(newReaction)
          legendary_action_entries = []
          for legendary_action in monster['legendary_actions']:
            newLegendaryAction = LegendaryAction( desc = legendary_action['desc'],
                                                  name = legendary_action['name'] )
            legendary_action_entries.append(newLegendaryAction)
          special_ability_entries = []
          for special_ability in monster['legendary_actions']:
            newSpecialAbility = LegendaryAction( desc = special_ability['desc'],
                                                  name = special_ability['name'] )
            special_ability_entries.append(newSpecialAbility)
          #print("slug: " + monster['actions'])
          speed = '"' + str(monster['speed']) + '"'
          skills = '"' + str(monster['skills']) + '"'
          actions_json = json.dumps([action.__dict__ for action in action_entries ])
          reactions_json = json.dumps([reaction.__dict__ for reaction in reaction_entries ])
          legendary_actions_json = json.dumps([legendary_action.__dict__ for legendary_action in legendary_action_entries ])
          special_abilities_json = json.dumps([special_ability.__dict__ for special_ability in special_ability_entries ])
  
          newMonster = Monster(slug = monster['slug'],
                                name = monster['name'],
                                size = monster['size'],
                                type = monster['type'],
                                subtype = monster['subtype'],
                                group = monster['group'],
                                alignment = monster['alignment'],
                                armor_class = monster['armor_class'],
                                armor_desc = monster['armor_desc'],
                                hit_points = monster['hit_points'],
                                hit_dice = monster['hit_dice'],
                                speed = speed,
                                strength = monster['strength'],
                                dexterity = monster['dexterity'],
                                constitution = monster['constitution'],
                                intelligence = monster['intelligence'],
                                wisdom = monster['wisdom'],
                                charisma = monster['charisma'],
                                strength_save = monster['strength_save'],
                                dexterity_save = monster['dexterity_save'],
                                constitution_save = monster['constitution_save'],
                                intelligence_save = monster['intelligence_save'],
                                wisdom_save = monster['wisdom_save'],
                                charisma_save = monster['charisma_save'],
                                perception = monster['perception'],
                                skills = skills,
                                damage_vulnerabilities = monster['damage_vulnerabilities'],
                                damage_resistances = monster['damage_resistances'],
                                damage_immunities = monster['damage_immunities'],
                                condition_immunities = monster['condition_immunities'],
                                senses = monster['senses'],
                                languages = monster['languages'],
                                challenge_rating = monster['challenge_rating'],
                                #actions = "",
                                #reactions = "",
                                actions = actions_json,
                                reactions = reactions_json,
                                legendary_desc = monster['legendary_desc'],
                                #legendary_actions = "",
                                #special_abilities = "",
                                legendary_actions = legendary_actions_json,
                                special_abilities = special_abilities_json,
                                spell_list = "",
                                img_main = monster['img_main'],
                                document__slug = monster['document__slug'],
                                document__title = monster['document__title'],
                                document__license_url = monster['document__license_url']
          )
          monster_entries.append(newMonster)
          
          if newMonster:
            exists = Monster.query.filter_by(slug=newMonster.slug).first()
            if not exists:
              print("Adding monster: " + newMonster.slug)
              db.session.add(newMonster)
        db.session.commit()